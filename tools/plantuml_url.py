# -*- coding: utf-8 -*-
"""Codifica un .puml en una URL de plantuml.com (deflate + base64 del alfabeto de PlantUML).

    python3 tools/plantuml_url.py docs/diagrama-de-clases.puml

Devuelve tres enlaces del mismo diagrama: el editor (editable en linea), el PNG y el SVG.
No requiere cuenta ni instalar nada.
"""

import base64
import sys
import zlib

ESTANDAR = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
PLANTUML = b"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
TABLA = bytes.maketrans(ESTANDAR, PLANTUML)
SERVIDOR = "https://www.plantuml.com/plantuml"


def codificar(texto):
    crudo = zlib.compress(texto.encode("utf-8"), 9)[2:-4]      # deflate sin cabecera zlib
    return base64.b64encode(crudo).translate(TABLA).rstrip(b"=").decode("ascii")


def enlaces(ruta):
    clave = codificar(open(ruta, encoding="utf-8").read())
    return {
        "editor": f"{SERVIDOR}/uml/{clave}",
        "png": f"{SERVIDOR}/png/{clave}",
        "svg": f"{SERVIDOR}/svg/{clave}",
        "longitud": len(clave),
    }


if __name__ == "__main__":
    ruta = sys.argv[1] if len(sys.argv) > 1 else "docs/diagrama-de-clases.puml"
    for k, v in enlaces(ruta).items():
        print(f"{k}: {v}")
