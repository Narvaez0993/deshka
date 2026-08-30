# -*- coding: utf-8 -*-
"""Publica el catalogo como issues de GitHub y los carga en el project.

    python3 tools/generate.py && python3 tools/publish.py

Idempotencia: si un issue con el mismo titulo ya existe, no se vuelve a crear.
"""

import json
import os
import subprocess
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OWNER, REPO = "Narvaez0993", "deshka"
PROJECT_ID = "PVT_kwHOA6dfgs4Bh8XU"
LOTE = 8


def gh_graphql(query, variables):
    payload = os.path.join(BASE, ".build", "_payload.json")
    with open(payload, "w", encoding="utf-8") as fh:
        json.dump({"query": query, "variables": variables}, fh, ensure_ascii=False)
    out = subprocess.run(["gh", "api", "graphql", "--input", payload],
                         capture_output=True, text=True)
    if out.returncode != 0:
        raise SystemExit(f"GraphQL fallo:\n{out.stdout}\n{out.stderr}")
    data = json.loads(out.stdout)
    if "errors" in data:
        raise SystemExit("GraphQL errores: " + json.dumps(data["errors"], ensure_ascii=False)[:2000])
    return data["data"]


def cargar_contexto():
    ids = json.load(open(os.path.join(BASE, ".build", "repo_ids.json")))["data"]["repository"]
    campos = {f["name"]: f for f in
              json.load(open(os.path.join(BASE, ".build", "fields.json")))["fields"]}
    return {
        "repo_id": ids["id"],
        "labels": {n["name"]: n["id"] for n in ids["labels"]["nodes"]},
        "milestones": {n["title"]: n["id"] for n in ids["milestones"]["nodes"]},
        "campos": campos,
    }


def opcion(campos, campo, nombre):
    for o in campos[campo]["options"]:
        if o["name"] == nombre:
            return o["id"]
    raise SystemExit(f"opcion no encontrada: {campo} / {nombre}")


def existentes():
    out = subprocess.run(["gh", "issue", "list", "--repo", f"{OWNER}/{REPO}",
                          "--limit", "300", "--state", "all",
                          "--json", "title,id,url,number,body"],
                         capture_output=True, text=True, check=True)
    return {i["title"]: i for i in json.loads(out.stdout)}


def sincronizar_cuerpos(historias, ya):
    """Reescribe el cuerpo de los issues cuyo texto cambio desde la ultima generacion."""
    cambiados = []
    for h in historias:
        actual = ya.get(h["titulo"])
        if not actual:
            continue
        nuevo = open(os.path.join(BASE, h["cuerpo"]), encoding="utf-8").read().rstrip()
        if (actual.get("body") or "").rstrip() != nuevo:
            cambiados.append((actual["id"], nuevo))
    for i in range(0, len(cambiados), LOTE):
        grupo = cambiados[i:i + LOTE]
        partes, variables, firmas = [], {}, []
        for n, (iid, cuerpo) in enumerate(grupo):
            variables[f"i{n}"], variables[f"b{n}"] = iid, cuerpo
            firmas += [f"$i{n}:ID!", f"$b{n}:String!"]
            partes.append(f'  e{n}: updateIssue(input:{{id:$i{n}, body:$b{n}}}) '
                          f'{{ issue {{ number }} }}')
        gh_graphql("mutation(" + ", ".join(firmas) + ") {\n" + "\n".join(partes) + "\n}", variables)
        print(f"  cuerpos actualizados {i + len(grupo)}/{len(cambiados)}")
    if not cambiados:
        print("  cuerpos al dia")
    return len(cambiados)


def crear_issues(historias, ctx, ya):
    creados = {}
    pendientes = [h for h in historias if h["titulo"] not in ya]
    for i in range(0, len(pendientes), LOTE):
        grupo = pendientes[i:i + LOTE]
        partes, variables = [], {"repo": ctx["repo_id"]}
        firmas = ["$repo:ID!"]
        for n, h in enumerate(grupo):
            cuerpo = open(os.path.join(BASE, h["cuerpo"]), encoding="utf-8").read()
            variables[f"t{n}"] = h["titulo"]
            variables[f"b{n}"] = cuerpo
            variables[f"l{n}"] = [ctx["labels"][x] for x in h["labels"]]
            variables[f"m{n}"] = ctx["milestones"][h["release_nombre"]]
            firmas += [f"$t{n}:String!", f"$b{n}:String!", f"$l{n}:[ID!]", f"$m{n}:ID"]
            partes.append(
                f'  c{n}: createIssue(input:{{repositoryId:$repo, title:$t{n}, body:$b{n}, '
                f'labelIds:$l{n}, milestoneId:$m{n}}}) {{ issue {{ id number url title }} }}')
        query = "mutation(" + ", ".join(firmas) + ") {\n" + "\n".join(partes) + "\n}"
        data = gh_graphql(query, variables)
        for n, h in enumerate(grupo):
            creados[h["id"]] = data[f"c{n}"]["issue"]
        print(f"  issues {i + len(grupo)}/{len(pendientes)}")
    return creados


def al_project(historias, issues, ctx):
    campos = ctx["campos"]
    items = {}
    ids = [(h["id"], issues[h["id"]]["id"]) for h in historias if h["id"] in issues]
    for i in range(0, len(ids), LOTE):
        grupo = ids[i:i + LOTE]
        partes, variables, firmas = [], {"p": PROJECT_ID}, ["$p:ID!"]
        for n, (hu, cid) in enumerate(grupo):
            variables[f"c{n}"] = cid
            firmas.append(f"$c{n}:ID!")
            partes.append(f'  a{n}: addProjectV2ItemById(input:{{projectId:$p, contentId:$c{n}}}) '
                          f'{{ item {{ id }} }}')
        data = gh_graphql("mutation(" + ", ".join(firmas) + ") {\n" + "\n".join(partes) + "\n}",
                          variables)
        for n, (hu, _) in enumerate(grupo):
            items[hu] = data[f"a{n}"]["item"]["id"]
        print(f"  al tablero {i + len(grupo)}/{len(ids)}")

    por_hu = {h["id"]: h for h in historias}
    valores = []
    for hu, item in items.items():
        h = por_hu[hu]
        req = ", ".join(h["ru"]) + " · " + (", ".join(h["rf"]) if h["rf"] else "sin RF")
        valores += [
            (item, campos["Status"]["id"], "opt", opcion(campos, "Status", "Todo")),
            (item, campos["Release"]["id"], "opt", opcion(campos, "Release", h["release_nombre"])),
            (item, campos["Actividad"]["id"], "opt", opcion(campos, "Actividad", h["actividad_nombre"])),
            (item, campos["Tarea"]["id"], "txt", h["tarea"]),
            (item, campos["Requisitos"]["id"], "txt", req),
        ]
    for i in range(0, len(valores), 20):
        grupo = valores[i:i + 20]
        partes, variables, firmas = [], {"p": PROJECT_ID}, ["$p:ID!"]
        for n, (item, campo, tipo, valor) in enumerate(grupo):
            variables[f"i{n}"], variables[f"f{n}"] = item, campo
            firmas += [f"$i{n}:ID!", f"$f{n}:ID!"]
            if tipo == "opt":
                variables[f"v{n}"] = valor
                firmas.append(f"$v{n}:String!")
                val = "{singleSelectOptionId:$v%d}" % n
            else:
                variables[f"v{n}"] = valor
                firmas.append(f"$v{n}:String!")
                val = "{text:$v%d}" % n
            partes.append(f'  u{n}: updateProjectV2ItemFieldValue(input:{{projectId:$p, '
                          f'itemId:$i{n}, fieldId:$f{n}, value:{val}}}) '
                          f'{{ projectV2Item {{ id }} }}')
        gh_graphql("mutation(" + ", ".join(firmas) + ") {\n" + "\n".join(partes) + "\n}", variables)
        print(f"  campos {i + len(grupo)}/{len(valores)}")
    return items


if __name__ == "__main__":
    manifest = json.load(open(os.path.join(BASE, ".build", "manifest.json"), encoding="utf-8"))
    historias = manifest["historias"]
    ctx = cargar_contexto()
    ya = existentes()
    print(f"{len(historias)} historias · {len(ya)} issues ya existen")
    sincronizar_cuerpos(historias, ya)
    issues = crear_issues(historias, ctx, ya)
    for h in historias:
        if h["titulo"] in ya and h["id"] not in issues:
            issues[h["id"]] = ya[h["titulo"]]
    al_project(historias, issues, ctx)
    print(f"listo: {len(issues)} historias publicadas")
