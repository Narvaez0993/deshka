# -*- coding: utf-8 -*-
"""Genera el catalogo Markdown y los cuerpos de los issues a partir de las historias.

    python3 tools/generate.py

Salidas:
    historias/NN-*.md          catalogo por actividad
    historias/README.md        indice de las historias
    docs/trazabilidad.md       RU / RF -> HU
    docs/story-map.md          el mapa en texto
    .build/issues/HU-XX.md     cuerpo de cada issue
    .build/manifest.json       metadatos para crear los issues y el project
"""

import json
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "tools"))

from model import ACTIVIDADES, RELEASES          # noqa: E402
import data_01_02, data_03, data_04_05, data_06_07, data_08_09   # noqa: E402

HISTORIAS = (data_01_02.HU + data_03.HU + data_04_05.HU
             + data_06_07.HU + data_08_09.HU)

SLUG_ACTIVIDAD = {
    "01": "empezar-a-usar-deshka",
    "02": "configurar-mi-dinero",
    "03": "registrar-lo-que-pasa",
    "04": "revisar-mi-dia-a-dia",
    "05": "ponerme-limites",
    "06": "cuidar-mis-compromisos",
    "07": "ahorrar-con-proposito",
    "08": "entender-y-decidir",
    "09": "administrar-mi-cuenta-y-mi-plan",
}

REL_LABEL = {"R1": "release-1-mvp", "R2": "release-2-sin-friccion", "R3": "release-3-agente"}
REL_COLOR = {"R1": "0E8A16", "R2": "D4A017", "R3": "5B4FCF"}
ACT_COLOR = "1F3864"


def escribir(ruta, contenido):
    destino = os.path.join(BASE, ruta)
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, "w", encoding="utf-8") as fh:
        fh.write(contenido.rstrip() + "\n")
    return ruta


def por_actividad():
    grupos = {}
    for h in HISTORIAS:
        grupos.setdefault(h.actividad, []).append(h)
    return grupos


def catalogo():
    rutas = []
    for act, historias in sorted(por_actividad().items()):
        nombre, descripcion = ACTIVIDADES[act]
        p = [f"# {act} · {nombre}", "", f"*{descripcion}*", ""]
        tareas = []
        for h in historias:
            if h.tarea not in tareas:
                tareas.append(h.tarea)
        p.append("**Tareas del story map:** " + " · ".join(f"«{t}»" for t in tareas))
        p.append("")
        p.append("| Historia | Título | Release | RF |")
        p.append("|---|---|---|---|")
        for h in historias:
            rf = ", ".join(h.rf) if h.rf else "— *sin RF*"
            p.append(f"| `{h.id}` | {h.titulo} | {RELEASES[h.release][0]} | {rf} |")
        p.append("")
        p.append("---")
        p.append("")
        for h in historias:
            p.append(h.cuerpo())
            p.append("")
            p.append("---")
            p.append("")
        rutas.append(escribir(f"historias/{act}-{SLUG_ACTIVIDAD[act]}.md", "\n".join(p)))
    return rutas


def indice():
    p = ["# Catálogo de historias de usuario", "",
         f"**{len(HISTORIAS)} historias** organizadas según el story map: "
         "9 actividades del recorrido del usuario × 3 releases.",
         "",
         "Cada historia trae sus criterios de aceptación en **Gherkin** y su trazabilidad "
         "hacia los requisitos del Entregable #1 (RU, RF, RN, RNF).",
         ""]
    for act, historias in sorted(por_actividad().items()):
        nombre, descripcion = ACTIVIDADES[act]
        archivo = f"{act}-{SLUG_ACTIVIDAD[act]}.md"
        p.append(f"## {act} · [{nombre}](./{archivo})")
        p.append("")
        p.append(f"*{descripcion}*")
        p.append("")
        p.append("| Historia | Título | Tarea | Release | RU | RF |")
        p.append("|---|---|---|---|---|---|")
        for h in historias:
            rf = ", ".join(h.rf) if h.rf else "— *sin RF*"
            p.append(f"| [`{h.id}`](./{archivo}#{h.ancla}) | {h.titulo} | {h.tarea} | "
                     f"{RELEASES[h.release][0]} | {', '.join(h.ru)} | {rf} |")
        p.append("")
    return escribir("historias/README.md", "\n".join(p))


def trazabilidad():
    ru_map, rf_map = {}, {}
    for h in HISTORIAS:
        for ru in h.ru:
            ru_map.setdefault(ru, []).append(h)
        for rf in h.rf:
            rf_map.setdefault(rf, []).append(h)

    # Cobertura parcial vigente. En el Entregable 2, RF-54 y RF-55 cerraron la brecha de RU-18,
    # y RNF-24 con RN-30 cerraron la de RU-17.
    PARCIALES = {}

    p = ["# Trazabilidad — requisitos ↔ historias de usuario", "",
         "Cierra el ciclo del numeral 1.5 del Entregable #1, con los requisitos refinados en el "
         "Entregable #2: cada requisito de usuario y cada requisito funcional queda enlazado con "
         "las historias que lo implementan.",
         "",
         "## Requisitos de usuario → historias", "",
         "| RU | Historias | Cobertura |", "|---|---|---|"]
    for n in range(1, 21):
        ru = f"RU-{n:02d}"
        hs = ru_map.get(ru, [])
        ids = ", ".join(f"`{h.id}`" for h in hs) if hs else "—"
        if not hs:
            cobertura = "Sin cobertura"
        elif ru in PARCIALES:
            cobertura = f"Parcial — {PARCIALES[ru]}"
        else:
            cobertura = "Completa"
        p.append(f"| {ru} | {ids} | {cobertura} |")

    p += ["", "## Requisitos funcionales → historias", "",
          "| RF | Historias |", "|---|---|"]
    for n in range(1, 59):
        rf = f"RF-{n:02d}"
        hs = rf_map.get(rf, [])
        ids = ", ".join(f"`{h.id}`" for h in hs) if hs else "— *sin historia*"
        p.append(f"| {rf} | {ids} |")

    huerfanas = [h for h in HISTORIAS if not h.rf]
    p += ["", "## Historias sin requisito funcional", "",
          "Aparecen en el story map porque el usuario las espera, pero todavía no tienen un RF "
          "escrito: son las brechas que la matriz del numeral 1.5 marca como cobertura parcial.",
          "", "| Historia | Título | RU afectado |", "|---|---|---|"]
    for h in huerfanas:
        p.append(f"| `{h.id}` | {h.titulo} | {', '.join(h.ru)} |")
    if not huerfanas:
        p[-4:] = ["Ninguna: desde el Entregable 2 todas las historias tienen al menos un requisito "
                  "funcional (RF-54 y RF-55 cerraron las dos brechas que quedaban)."]
    return escribir("docs/trazabilidad.md", "\n".join(p))


def story_map():
    p = ["# Story map", "",
         "El recorrido del usuario de izquierda a derecha; hacia abajo, las funcionalidades "
         "ordenadas por release. Cada tarjeta del mapa corresponde a **una** historia de este "
         "catálogo.", "",
         "![Story map de Deshka](../assets/story-map.png)", ""]
    for rel in ("R1", "R2", "R3"):
        nombre, sub = RELEASES[rel]
        p.append(f"## {nombre} — {sub}")
        p.append("")
        for act, historias in sorted(por_actividad().items()):
            del_rel = [h for h in historias if h.release == rel]
            if not del_rel:
                continue
            p.append(f"**{act} · {ACTIVIDADES[act][0]}**")
            p.append("")
            for h in del_rel:
                rf = ", ".join(h.rf) if h.rf else "sin RF definido"
                p.append(f"- `{h.id}` {h.titulo} — *{rf}*")
            p.append("")
    p += ["## El corte del MVP", "",
          "El Release 1 entrega la promesa mínima defendible: registrar todo el dinero que entra "
          "y sale, con la tarjeta de crédito bien contabilizada, medirse contra un tope propio y "
          "recibir el corte del mes, que es la primera vez que el agente explica en lugar de solo "
          "mostrar. Sin captura asistida todavía, porque un registro manual correcto vale más que "
          "uno automático que nadie puede corregir."]
    return escribir("docs/story-map.md", "\n".join(p))


def issues():
    manifest = []
    for h in HISTORIAS:
        cuerpo = []
        cuerpo.append(h.cuerpo(con_encabezado=False))
        cuerpo.append("")
        cuerpo.append("---")
        cuerpo.append(f"<sub>Catálogo completo: "
                      f"[`historias/{h.actividad}-{SLUG_ACTIVIDAD[h.actividad]}.md`]"
                      f"(../blob/main/historias/{h.actividad}-{SLUG_ACTIVIDAD[h.actividad]}.md) · "
                      f"Deshka · Entregable #1, numeral 3.</sub>")
        ruta = escribir(f".build/issues/{h.id}.md", "\n".join(cuerpo))
        manifest.append({
            "id": h.id,
            "titulo": f"{h.id} · {h.titulo}",
            "cuerpo": ruta,
            "actividad": h.actividad,
            "actividad_nombre": f"{h.actividad} · {ACTIVIDADES[h.actividad][0]}",
            "tarea": h.tarea,
            "release": h.release,
            "release_nombre": RELEASES[h.release][0],
            "labels": [
                f"actividad-{h.actividad}-{SLUG_ACTIVIDAD[h.actividad]}",
                REL_LABEL[h.release],
                "historia-de-usuario",
            ] + ([] if h.rf else ["sin-rf"]),
            "ru": h.ru,
            "rf": h.rf,
        })
    escribir(".build/manifest.json", json.dumps({
        "historias": manifest,
        "labels": (
            [{"name": f"actividad-{a}-{SLUG_ACTIVIDAD[a]}",
              "color": ACT_COLOR,
              "desc": f"Actividad {a} del story map: {ACTIVIDADES[a][0]}"} for a in sorted(ACTIVIDADES)]
            + [{"name": REL_LABEL[r], "color": REL_COLOR[r],
                "desc": f"{RELEASES[r][0]} — {RELEASES[r][1]}"} for r in ("R1", "R2", "R3")]
            + [{"name": "historia-de-usuario", "color": "6E7781",
                "desc": "Historia de usuario con criterios de aceptacion en Gherkin"},
               {"name": "sin-rf", "color": "B60205",
                "desc": "Brecha: la historia aun no tiene requisito funcional escrito"}]
        ),
        "milestones": [{"title": RELEASES[r][0], "desc": RELEASES[r][1]} for r in ("R1", "R2", "R3")],
    }, ensure_ascii=False, indent=2))
    return manifest


if __name__ == "__main__":
    ids = [h.id for h in HISTORIAS]
    assert len(ids) == len(set(ids)), "hay identificadores repetidos"
    esperados = [f"HU-{n:02d}" for n in range(1, len(ids) + 1)]
    assert ids == esperados, f"numeracion no consecutiva: {set(esperados) ^ set(ids)}"
    catalogo()
    indice()
    trazabilidad()
    story_map()
    m = issues()
    print(f"{len(m)} historias generadas")
    print(f"  escenarios: {sum(len(h.escenarios) for h in HISTORIAS)}")
    print(f"  pasos Gherkin: {sum(len(p) for h in HISTORIAS for _, p in h.escenarios)}")
