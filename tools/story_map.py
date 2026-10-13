# -*- coding: utf-8 -*-
"""Genera el story map a partir del catálogo de historias (tools/data_*.py).

    python3 tools/story_map.py            # escribe assets/story-map.html
    python3 tools/story_map.py --png      # además lo exporta a assets/story-map.png con Chrome

El estado de cada historia se lee en vivo del project de GitHub con `gh`; sin `gh`, todas
aparecen como pendientes. ETIQUETAS marca lo que cambió frente al Entregable 1.
"""

import html
import json
import os
import subprocess
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESHKA_TOOLS = os.path.join(BASE, "tools")
AQUI = os.path.join(BASE, "assets")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ANCHO = 2480

sys.path.insert(0, DESHKA_TOOLS)
import model  # noqa: E402
import data_01_02, data_03, data_04_05, data_06_07, data_08_09  # noqa: E402,E401

HISTORIAS = data_01_02.HU + data_03.HU + data_04_05.HU + data_06_07.HU + data_08_09.HU

# --------------------------------------------------------------------------------------
# Cambios propuestos en la revisión del story map (Entregable 2)
# --------------------------------------------------------------------------------------

ACTIVIDADES = model.ACTIVIDADES

# Orden de las tareas de cada actividad (la fila de tareas del mapa).
TAREAS = {
    "01": ["Crear mi cuenta", "Entrar", "Contar qué quiero lograr"],
    "02": ["Registrar mis fuentes", "Organizar categorías"],
    "03": ["Capturar el movimiento", "Confirmar lo que entendió"],
    "04": ["Ver cómo voy", "Depurar el historial"],
    "05": ["Definir el tope", "Seguir el consumo"],
    "06": ["Suscripciones", "Deudas con personas"],
    "07": ["Crear la meta", "Mover plata a la meta", "Seguir y cerrar la meta"],
    "08": ["Recibir avisos", "Conversar con el agente", "Recibir mis resúmenes", "Aplicar lo que propone"],
    "09": ["Ajustar mi cuenta", "Ver mi consumo", "Mejorar el plan", "Llevarme o borrar mis datos"],
}

# Cambios frente al story map del Entregable 1 (ver docs/story-map.md).
ETIQUETAS = {
    "HU-01": "ajustada", "HU-04": "movida", "HU-05": "ajustada", "HU-06": "ajustada",
    "HU-43": "movida", "HU-44": "movida", "HU-46": "movida", "HU-47": "al MVP",
    "HU-48": "movida", "HU-49": "movida", "HU-50": "movida", "HU-54": "movida",
    "HU-55": "nueva",
}

RELEASES = {
    "R1": dict(
        nombre="Release 1 · MVP", lema="Registrar y entender lo básico",
        objetivo="Que todo lo que entra y sale quede registrado, con la tarjeta bien contada, "
                 "y que el usuario se mida contra un tope propio y reciba la explicación de su mes.",
        metrica="En su primer mes registra movimientos al menos 5 días por semana y su saldo "
                "neto coincide con el real.",
        color="#1F7A4D", fondo="#EAF5EE"),
    "R2": dict(
        nombre="Release 2 · Sin fricción", lema="Captura asistida y control del gasto",
        objetivo="Registrar en segundos hablando o escribiendo, y controlar el gasto con topes, "
                 "compromisos y metas.",
        metrica="Al menos 6 de cada 10 movimientos entran por voz o texto, y el registro por voz "
                "tarda menos de 5 s (RNF-01).",
        color="#A86A12", fondo="#FBF2E4"),
    "R3": dict(
        nombre="Release 3 · Agente", lema="El sistema trabaja por el usuario",
        objetivo="Que el agente revise, avise y proponga sin que el usuario se lo pida.",
        metrica="Al menos la mitad de los usuarios abre su revisión semanal y aplica una jugada "
                "al mes.",
        color="#5B3FB0", fondo="#F0ECFA"),
}

ESTADOS = {
    "Done": ("Hecha", "#1F7A4D", "#E3F3E9", "✓"),
    "In Progress": ("En progreso", "#A86A12", "#FBEFD9", "◐"),
    "Todo": ("Pendiente", "#5A6475", "#EEF0F3", "○"),
    "Nueva": ("Nueva", "#5A6475", "#EEF0F3", "○"),
}


def historias_finales():
    return [(h, ETIQUETAS.get(h.id), h.id in ETIQUETAS) for h in HISTORIAS]


def etiqueta_cambio(h, etiqueta):
    return etiqueta


def estado_tablero():
    """Estado de cada historia en el project de GitHub (Todo / In Progress / Done)."""
    try:
        out = subprocess.run(["gh", "project", "item-list", "3", "--owner", "Narvaez0993",
                              "--limit", "300", "--format", "json"],
                             capture_output=True, text=True, timeout=60, check=True).stdout
        return {i["title"].split(" ")[0]: i.get("status") or "Todo" for i in json.loads(out)["items"]}
    except Exception:
        return {}


def tarjeta(h, cambio, estado):
    e = ESTADOS[estado]
    rf = " · ".join(h.rf) if h.rf else "sin RF"
    cambio_html = f'<span class="cambio">{html.escape(cambio)}</span>' if cambio else ""
    clase_nueva = " nueva" if cambio == "nueva" else ""
    return f"""
      <div class="card r{h.release[-1]}{clase_nueva}">
        <div class="card-top"><span class="hu">{h.id}</span>{cambio_html}</div>
        <div class="titulo">{html.escape(h.titulo)}</div>
        <div class="tarea">{html.escape(h.tarea)}</div>
        <div class="card-bottom">
          <span class="rf">{html.escape(rf)}</span>
          <span class="estado" style="color:{e[1]};background:{e[2]}">{e[3]} {e[0]}</span>
        </div>
      </div>"""


def generar_html():
    estado_tablero = estado_tablero_cache
    finales = historias_finales()
    columnas = list(ACTIVIDADES.keys())

    def orden(item):
        h = item[0]
        return (TAREAS[h.actividad].index(h.tarea), int(h.id[3:]))

    cabecera = "".join(
        f'<div class="actividad"><span class="num">{k}</span>{html.escape(ACTIVIDADES[k][0])}</div>'
        for k in columnas)
    tareas = "".join(
        '<div class="tareas">' + "".join(f'<div class="t">{html.escape(t)}</div>' for t in TAREAS[k]) + "</div>"
        for k in columnas)

    carriles = []
    for rid, r in RELEASES.items():
        celdas = []
        for k in columnas:
            items = sorted([it for it in finales if it[0].release == rid and it[0].actividad == k], key=orden)
            if items:
                celdas.append('<div class="celda">' + "".join(
                    tarjeta(h, cambio, estado_tablero.get(h.id, "Todo")) for h, cambio, _ in items) + "</div>")
            else:
                celdas.append('<div class="celda vacia"><div class="hueco">—</div></div>')
        n = sum(1 for it in finales if it[0].release == rid)
        hechas = sum(1 for it in finales if it[0].release == rid and estado_tablero.get(it[0].id) == "Done")
        carriles.append(f"""
    <section class="carril" style="--c:{r['color']};--f:{r['fondo']}">
      <div class="lane-label">
        <div class="lane-nombre">{html.escape(r['nombre'])}</div>
        <div class="lane-lema">{html.escape(r['lema'])}</div>
        <div class="lane-k">Objetivo</div><div class="lane-t">{html.escape(r['objetivo'])}</div>
        <div class="lane-k">Cómo sabemos que se logró</div><div class="lane-t">{html.escape(r['metrica'])}</div>
        <div class="lane-cuenta">{n} historias · {hechas} hechas</div>
      </div>
      {''.join(celdas)}
    </section>""")

    total = len(finales)
    resumen = {k: sum(1 for h, _, _ in finales if estado_tablero.get(h.id, "Todo") == k) for k in ESTADOS}

    return f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<title>Deshka · Story Mapping</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: #F6F7F9; color: #1A202C;
         font-family: -apple-system, "Helvetica Neue", Helvetica, Arial, sans-serif; }}
  .page {{ width: {ANCHO}px; padding: 40px 40px 36px; }}
  .eyebrow {{ font-size: 13px; letter-spacing: .12em; color: #6B7280; text-transform: uppercase; }}
  h1 {{ font-size: 34px; font-weight: 600; margin: 6px 0 10px; }}
  .intro {{ display: flex; gap: 28px; align-items: flex-start; justify-content: space-between; }}
  .lead {{ font-size: 16px; color: #4A5568; max-width: 720px; line-height: 1.45; margin: 0; }}
  .persona {{ background: #fff; border: 1px solid #DDE1E7; border-radius: 10px; padding: 14px 18px;
             max-width: 760px; font-size: 14.5px; line-height: 1.45; color: #2D3748; }}
  .persona b {{ color: #1A202C; }}
  .leyenda {{ display: flex; flex-direction: column; gap: 8px; font-size: 13px; color: #4A5568; min-width: 520px; }}
  .leyenda .fila {{ display: flex; gap: 16px; flex-wrap: wrap; align-items: center; }}
  .sw {{ display: inline-block; width: 12px; height: 12px; border-radius: 3px; margin-right: 6px; vertical-align: -1px; }}
  .pill {{ border-radius: 999px; padding: 2px 8px; font-size: 12px; font-weight: 600; }}
  .grid {{ display: grid; grid-template-columns: 250px repeat(9, 1fr); gap: 10px; margin-top: 26px; }}
  .rotulo {{ font-size: 12px; letter-spacing: .1em; text-transform: uppercase; color: #6B7280; padding-top: 10px; }}
  .rotulo small {{ display:block; text-transform:none; letter-spacing:0; font-size:12.5px; color:#8A93A2; margin-top:4px; line-height:1.35; }}
  .actividad {{ background: #1E2A4A; color: #fff; border-radius: 8px; padding: 14px 12px; font-size: 15.5px;
               font-weight: 600; line-height: 1.25; min-height: 64px; display: flex; gap: 8px; align-items: flex-start; }}
  .actividad .num {{ font-size: 12px; opacity: .65; padding-top: 2px; font-weight: 500; }}
  .tareas {{ display: flex; flex-direction: column; gap: 6px; }}
  .tareas .t {{ background: #E9ECF1; border-radius: 6px; padding: 7px 10px; font-size: 13.5px; color: #374151; }}
  .carril {{ display: contents; }}
  .lane-label {{ background: var(--f); border-left: 5px solid var(--c); border-radius: 8px; padding: 14px 14px 12px; }}
  .lane-nombre {{ font-size: 13px; letter-spacing: .08em; text-transform: uppercase; color: var(--c); font-weight: 700; }}
  .lane-lema {{ font-size: 16px; font-weight: 600; margin: 4px 0 10px; color: #1A202C; }}
  .lane-k {{ font-size: 11.5px; text-transform: uppercase; letter-spacing: .06em; color: #6B7280; margin-top: 8px; }}
  .lane-t {{ font-size: 13px; line-height: 1.38; color: #2D3748; margin-top: 2px; }}
  .lane-cuenta {{ font-size: 12.5px; color: var(--c); font-weight: 600; margin-top: 12px; }}
  .celda {{ background: var(--f); border-radius: 8px; padding: 8px; display: flex; flex-direction: column; gap: 8px; }}
  .celda.vacia {{ align-items: stretch; }}
  .hueco {{ border: 1.5px dashed #CBD2DC; border-radius: 6px; color: #A0AAB8; text-align: center; padding: 10px; font-size: 14px; }}
  .card {{ background: #fff; border-radius: 7px; padding: 9px 10px 8px; border: 1px solid #E2E6EC;
          border-left: 4px solid var(--c); box-shadow: 0 1px 0 rgba(0,0,0,.03); }}
  .card.nueva {{ border-style: dashed; border-left-style: solid; }}
  .card-top {{ display: flex; justify-content: space-between; align-items: center; }}
  .hu {{ font-family: "SF Mono", Menlo, monospace; font-size: 11.5px; color: #6B7280; }}
  .cambio {{ font-size: 10.5px; font-weight: 700; text-transform: uppercase; letter-spacing: .05em;
            color: #1E2A4A; background: #E4E9F7; border-radius: 4px; padding: 1px 6px; }}
  .titulo {{ font-size: 14px; line-height: 1.3; margin: 4px 0 4px; color: #1A202C; }}
  .tarea {{ font-size: 11.5px; color: #8A93A2; margin-bottom: 6px; }}
  .card-bottom {{ display: flex; justify-content: space-between; align-items: center; gap: 6px; }}
  .rf {{ font-family: "SF Mono", Menlo, monospace; font-size: 11px; color: #4A5568; }}
  .estado {{ border-radius: 999px; padding: 2px 7px; font-size: 11px; font-weight: 600; white-space: nowrap; }}
  .notas {{ display: grid; grid-template-columns: 1fr 1fr; gap: 28px; margin-top: 28px; border-top: 1px solid #DDE1E7;
           padding-top: 18px; font-size: 13.5px; line-height: 1.5; color: #4A5568; }}
  .notas b {{ color: #1A202C; }}
</style></head>
<body><div class="page">
  <div class="eyebrow">Deshka · Story Mapping (refinado en el Entregable 2)</div>
  <h1>Story Mapping</h1>
  <div class="intro">
    <div>
      <p class="lead">El recorrido del usuario de izquierda a derecha y, hacia abajo, las historias ordenadas por release.
        Cada tarjeta cita su requisito funcional, la tarea del usuario a la que responde y su estado en el tablero.</p>
      <div class="persona" style="margin-top:14px">
        <b>Para quién:</b> Ana, 28 años, empleada en Medellín. Paga casi todo con tarjeta y ha abandonado dos veces
        su Excel de gastos porque registrar cansa y los números nunca cuadran.<br>
        <b>Para qué:</b> saber cuánto dinero tiene de verdad, en qué se le va y si va a llegar a sus metas,
        sin digitar todo ni saber de finanzas.
      </div>
    </div>
    <div class="leyenda">
      <div class="fila">
        <span><span class="sw" style="background:#1F7A4D"></span>Release 1 · MVP</span>
        <span><span class="sw" style="background:#A86A12"></span>Release 2 · Sin fricción</span>
        <span><span class="sw" style="background:#5B3FB0"></span>Release 3 · Agente</span>
      </div>
      <div class="fila">
        <span class="pill" style="color:#1F7A4D;background:#E3F3E9">✓ Hecha · {resumen['Done']}</span>
        <span class="pill" style="color:#A86A12;background:#FBEFD9">◐ En progreso · {resumen['In Progress']}</span>
        <span class="pill" style="color:#5A6475;background:#EEF0F3">○ Pendiente · {resumen['Todo'] + resumen['Nueva']}</span>
        <span style="color:#6B7280">{total} historias en total</span>
      </div>
      <div class="fila">
        <span class="cambio">nueva</span><span class="cambio">movida</span><span class="cambio">al MVP</span>
        <span class="cambio">ajustada</span><span style="color:#6B7280">cambios frente al Entregable 1</span>
      </div>
    </div>
  </div>

  <div class="grid">
    <div class="rotulo">Actividades<small>El recorrido del usuario</small></div>
    {cabecera}
    <div class="rotulo">Tareas<small>Lo que hace en cada paso</small></div>
    {tareas}
    {''.join(carriles)}
  </div>

  <div class="notas">
    <div><b>Corte del MVP.</b> El Release 1 entrega la promesa mínima defendible: registrar todo el dinero que entra y sale,
      con la tarjeta de crédito bien contabilizada, medirse contra un tope propio y recibir el corte del mes, que es la
      primera vez que el agente explica en lugar de solo mostrar. Sin captura asistida todavía: un registro manual correcto
      vale más que uno automático que nadie puede corregir.</div>
    <div><b>Qué cambió frente al Entregable 1.</b> El mapa gana una persona y un objetivo medible por release. Las historias
      se reubican en la tarea que les corresponde: las preferencias pasan a la actividad 09, el seguimiento de la meta y los
      resúmenes del agente tienen tarea propia, y exportar pasa a «Llevarme o borrar mis datos». Se agrega la eliminación de
      la cuenta (HU-55). Las dos tarjetas sin requisito ya tienen RF (RF-54, RF-55), y el corte del mes entra al MVP.</div>
  </div>
</div>
<script>document.title = "H=" + document.querySelector('.page').scrollHeight;</script>
</body></html>"""


def exportar_png(ruta_html, ruta_png):
    url = "file://" + ruta_html
    dom = subprocess.run([CHROME, "--headless=new", "--disable-gpu", f"--window-size={ANCHO},2000",
                          "--virtual-time-budget=3000", "--dump-dom", url],
                         capture_output=True, text=True, timeout=120).stdout
    alto = int(dom.split("<title>H=")[1].split("<")[0]) + 10
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    f"--window-size={ANCHO},{alto}", "--force-device-scale-factor=1",
                    f"--screenshot={ruta_png}", url],
                   capture_output=True, text=True, timeout=120, check=True)
    return alto


if __name__ == "__main__":
    estado_tablero_cache = estado_tablero()
    ruta_html = os.path.join(AQUI, "story-map.html")
    with open(ruta_html, "w", encoding="utf-8") as fh:
        fh.write(generar_html())
    print("HTML:", ruta_html)
    if "--png" in sys.argv:
        alto = exportar_png(ruta_html, os.path.join(AQUI, "story-map.png"))
        print(f"PNG: {os.path.join(AQUI, 'story-map.png')} ({ANCHO}x{alto})")
