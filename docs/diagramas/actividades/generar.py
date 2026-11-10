"""Genera los diagramas de actividades del MVP en formato draw.io.

Por cada historia produce, en esta carpeta:
  - <hu>.drawio  el diagrama, editable en draw.io (escritorio o web)
  - <hu>.png     la imagen para el documento (exportada con la app de draw.io)
y escribe enlaces.md con el enlace editable de cada uno: un enlace de draw.io que lleva
el diagrama dentro, igual que «Exportar como URL», así que abre sin cuenta ni permisos.

Los pasos salen del código de la app y del backend (rama feature/entrega-3), con los
textos que se ven en pantalla.

Uso: python3 generar.py [hu-13 ...]   (sin argumentos genera todas y el archivo de enlaces)
"""

from __future__ import annotations

import base64
import html
import re
import subprocess
import sys
import urllib.parse
import zlib
from dataclasses import dataclass, field
from pathlib import Path

CARPETA = Path(__file__).parent
DRAWIO = next((str(p) for p in (Path("/Applications/draw.io.app/Contents/MacOS/draw.io"),
                                  *Path("/opt/homebrew/Caskroom/drawio").glob("*/draw.io.app/Contents/MacOS/draw.io"))
               if p.exists()), "/Applications/draw.io.app/Contents/MacOS/draw.io")

# --- Medidas y estilos -------------------------------------------------------------

ANCHO_CARRIL = 360
ALTO_CABECERA = 36
ANCHO_ACCION = 240
ANCHO_RAMA = 140
ANCHO_DECISION = 200
ANCHO_NOTA = 170
SEP_RAMAS = ANCHO_DECISION  # las ramas caen justo bajo las puntas del rombo
SEP_FILAS = 30

LETRA_ACCION = 13
LETRA_DECISION = 12
LETRA_NOTA = 12

COLORES_CARRIL = {
    "Usuario": "#E3F2FD",
    "App": "#E6F4EA",
    "API": "#EFE7FB",
    "Worker": "#FDEFE3",
}
TINTA = "#2D3748"

ESTILO = {
    "carril": f"swimlane;startSize={ALTO_CABECERA};html=1;fontStyle=1;fontSize=15;"
              f"strokeColor=#A0AEC0;swimlaneFillColor=#FCFCFD;",
    "accion": f"rounded=1;arcSize=24;whiteSpace=wrap;html=1;fontSize={LETRA_ACCION};"
              f"spacingLeft=6;spacingRight=6;fillColor=#FFFFFF;strokeColor={TINTA};",
    "decision": f"rhombus;whiteSpace=wrap;html=1;fontSize={LETRA_DECISION};spacingLeft=34;"
                f"spacingRight=34;fillColor=#FFF8E1;strokeColor=#B7791F;",
    "union": "rhombus;html=1;fillColor=#FFF8E1;strokeColor=#B7791F;",
    "inicio": f"ellipse;html=1;shape=startState;fillColor=#000000;strokeColor={TINTA};",
    "fin": f"ellipse;html=1;shape=endState;fillColor=#000000;strokeColor={TINTA};",
    "fin_flujo": f"shape=sumEllipse;perimeter=ellipsePerimeter;html=1;fillColor=#FFFFFF;"
                 f"strokeColor={TINTA};",
    "region": "rounded=1;arcSize=6;dashed=1;fillColor=none;strokeColor=#805AD5;"
              "verticalAlign=top;align=right;spacingRight=8;spacingTop=2;fontSize=12;"
              "fontColor=#553C9A;fontStyle=2;html=1;",
    "nota": f"shape=note;whiteSpace=wrap;html=1;size=14;fontSize={LETRA_NOTA};align=left;"
            f"spacingLeft=6;spacingRight=4;fillColor=#FFFBEA;strokeColor=#D69E2E;",
    "titulo": "text;html=1;fontSize=18;fontStyle=1;align=left;verticalAlign=middle;",
    "flecha": f"edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=open;endSize=9;"
              f"strokeColor={TINTA};fontSize=12;labelBackgroundColor=#FFFFFF;",
}

ALTOS_FIJOS = {"union": 28, "inicio": 28, "fin": 30, "fin_flujo": 26}


def lineas(texto: str, ancho_util: float, tam: int) -> int:
    """Cuántas líneas ocupa el texto, con el ancho promedio de un carácter de Helvetica."""
    por_caracter = tam * 0.53
    n, actual = 1, 0.0
    for palabra in texto.split():
        largo = len(palabra) * por_caracter
        if actual and actual + por_caracter + largo > ancho_util:
            n, actual = n + 1, largo
        else:
            actual += (por_caracter if actual else 0) + largo
    return n


def alto_accion(texto: str, ancho: float) -> float:
    n = lineas(texto, ancho - 20, LETRA_ACCION)
    return max(52, 20 + n * LETRA_ACCION * 1.3)


def alto_decision(texto: str) -> float:
    n = lineas(texto, ANCHO_DECISION - 72, LETRA_DECISION)
    return max(92, 32 + n * 30)


def alto_nota(texto: str) -> float:
    n = lineas(texto, ANCHO_NOTA - 20, LETRA_NOTA)
    return max(52, 20 + n * LETRA_NOTA * 1.3)


# --- Modelo del flujo -------------------------------------------------------------

@dataclass
class Paso:
    tipo: str            # inicio | accion | decision | fin | fin_flujo
    carril: str
    texto: str = ""
    ramas: list = field(default_factory=list)   # decisión: [(condición, [Paso, ...]), ...]


def inicio(carril="Usuario"):
    return Paso("inicio", carril)


def accion(carril, texto):
    return Paso("accion", carril, texto)


def decision(carril, pregunta, *ramas):
    return Paso("decision", carril, pregunta, list(ramas))


def fin(carril):
    return Paso("fin", carril)


def fin_flujo(carril):
    """Nodo de fin de flujo (⊗): termina ese camino sin terminar la actividad."""
    return Paso("fin_flujo", carril)


@dataclass
class Diagrama:
    clave: str
    titulo: str
    pasos: list
    carriles: list = field(default_factory=lambda: ["Usuario", "App", "API"])
    regiones: list = field(default_factory=list)   # [(texto, primer paso, último paso)]
    notas: list = field(default_factory=list)      # [(texto, índice del paso[, "izquierda"|"derecha"])]


# --- Construcción del XML de draw.io ----------------------------------------------

class Lienzo:
    def __init__(self):
        self.celdas = []
        self.siguiente = 2

    def _id(self):
        self.siguiente += 1
        return f"c{self.siguiente}"

    def vertice(self, estilo, x, y, ancho, alto, texto=""):
        cid = self._id()
        texto = re.sub(r"\b(RNF|RN|RF|RU|HU)-(\d)", "\\1\u2011\\2", texto)
        self.celdas.append(
            f'<mxCell id="{cid}" value="{html.escape(texto, quote=True)}" style="{estilo}" '
            f'vertex="1" parent="1"><mxGeometry x="{x:.0f}" y="{y:.0f}" width="{ancho:.0f}" '
            f'height="{alto:.0f}" as="geometry"/></mxCell>'
        )
        return cid

    def arista(self, origen, destino, etiqueta="", salida=None, entrada=None, recta=False,
               estilo=None):
        cid = self._id()
        estilo = estilo or ESTILO["flecha"]
        if recta:
            estilo = estilo.replace("edgeStyle=orthogonalEdgeStyle;", "")
        if salida:
            estilo += f"exitX={salida[0]};exitY={salida[1]};exitDx=0;exitDy=0;"
        if entrada:
            estilo += f"entryX={entrada[0]};entryY={entrada[1]};entryDx=0;entryDy=0;"
        self.celdas.append(
            f'<mxCell id="{cid}" value="{html.escape(etiqueta, quote=True)}" style="{estilo}" '
            f'edge="1" parent="1" source="{origen}" target="{destino}">'
            f'<mxGeometry relative="1" as="geometry"/></mxCell>'
        )

    def xml(self, nombre):
        cuerpo = "".join(self.celdas)
        return (
            f'<mxfile host="drawio"><diagram name="{html.escape(nombre, quote=True)}" id="d1">'
            f'<mxGraphModel dx="1200" dy="900" grid="0" gridSize="10" guides="1" tooltips="1" '
            f'connect="1" arrows="1" fold="1" page="0" pageScale="1" math="0" shadow="0">'
            f'<root><mxCell id="0"/><mxCell id="1" parent="0"/>{cuerpo}</root>'
            f'</mxGraphModel></diagram></mxfile>'
        )


def medidas(paso: Paso, en_rama=False):
    if paso.tipo == "accion":
        ancho = ANCHO_RAMA if en_rama else ANCHO_ACCION
        return ancho, alto_accion(paso.texto, ancho)
    if paso.tipo == "decision":
        return ANCHO_DECISION, alto_decision(paso.texto)
    alto = ALTOS_FIJOS[paso.tipo]
    return alto, alto


def construir(d: Diagrama) -> str:
    lienzo = Lienzo()
    orden = d.carriles
    x0, y_titulo, y_carril = 20, 10, 56
    centro = {c: x0 + i * ANCHO_CARRIL + ANCHO_CARRIL / 2 for i, c in enumerate(orden)}

    # Primero se ubica todo para conocer la altura total: los carriles van antes en el
    # XML para quedar detrás.
    colocados = []   # (Paso, x, y, ancho, alto) de cada paso principal
    plan = []        # ("paso", i) o ("decision", i, ramas, unión)
    y = y_carril + ALTO_CABECERA + 26
    for i, paso in enumerate(d.pasos):
        cx = centro[paso.carril]
        ancho, alto = medidas(paso)
        colocados.append((paso, cx - ancho / 2, y, ancho, alto))
        y += alto + SEP_FILAS
        if paso.tipo != "decision":
            plan.append(("paso", i))
            continue
        ramas, y_ramas, alto_max = [], y, 0
        n = len(paso.ramas)
        for j, (condicion, subpasos) in enumerate(paso.ramas):
            desplazamiento = (j - (n - 1) / 2) * SEP_RAMAS
            yr, lista = y_ramas, []
            for sub in subpasos:
                sw, sh = medidas(sub, en_rama=True)
                scx = centro[sub.carril] + desplazamiento
                lista.append((sub, scx - sw / 2, yr, sw, sh))
                yr += sh + SEP_FILAS
            alto_max = max(alto_max, yr - y_ramas)
            abierta = not (subpasos and subpasos[-1].tipo in ("fin", "fin_flujo"))
            ramas.append((condicion, lista, abierta))
        y = y_ramas + alto_max
        union = None
        if sum(1 for r in ramas if r[2]) >= 2:
            union = (cx - 14, y, 28, 28)
            y += 28 + SEP_FILAS
        plan.append(("decision", i, ramas, union))

    alto_total = y - y_carril - 4

    lienzo.vertice(ESTILO["titulo"], x0, y_titulo, ANCHO_CARRIL * len(orden), 34, d.titulo)
    for i, nombre in enumerate(orden):
        estilo = ESTILO["carril"] + f"fillColor={COLORES_CARRIL.get(nombre, '#EDF2F7')};"
        lienzo.vertice(estilo, x0 + i * ANCHO_CARRIL, y_carril, ANCHO_CARRIL, alto_total, nombre)

    # Regiones punteadas (por ejemplo, una transacción), detrás de los pasos que encierran.
    for texto, a, b in d.regiones:
        cajas = [c[1:] for c in colocados[a:b + 1]]
        for entrada in plan:
            if entrada[0] == "decision" and a <= entrada[1] <= b:
                for _, lista, _ in entrada[2]:
                    cajas += [c[1:] for c in lista]
                if entrada[3]:
                    cajas.append(entrada[3])
        xs = [c[0] for c in cajas] + [c[0] + c[2] for c in cajas]
        ys = [c[1] for c in cajas] + [c[1] + c[3] for c in cajas]
        lienzo.vertice(ESTILO["region"], min(xs) - 8, min(ys) - 28,
                       max(xs) - min(xs) + 16, max(ys) - min(ys) + 40, texto)

    # Pasos y flechas. «pendientes» son los extremos que desembocan en el paso siguiente.
    ids = {}
    pendientes = []
    for entrada in plan:
        i = entrada[1]
        paso, x, yy, ancho, alto = colocados[i]
        ids[i] = lienzo.vertice(ESTILO[paso.tipo], x, yy, ancho, alto, paso.texto)
        for origen, etiqueta, salida in pendientes:
            lienzo.arista(origen, ids[i], etiqueta, salida)
        pendientes = [(ids[i], "", None)]
        if entrada[0] != "decision":
            continue
        _, _, ramas, union = entrada
        id_union = lienzo.vertice(ESTILO["union"], *union) if union else None
        ultima = len(ramas) - 1
        pendientes = []
        for j, (condicion, lista, abierta) in enumerate(ramas):
            # La rama izquierda sale por la punta izquierda del rombo y la derecha por la
            # derecha; cada una baja recta hasta su primera acción.
            punta = (0, 0.5) if j == 0 else (1, 0.5) if j == ultima else (0.5, 1)
            lado = (0, 0.5) if j == 0 else (1, 0.5) if j == ultima else (0.5, 0)
            etiqueta = f"[{condicion}]"
            anterior = ids[i]
            for k, (sub, sx, sy, sw, sh) in enumerate(lista):
                sid = lienzo.vertice(ESTILO[sub.tipo], sx, sy, sw, sh, sub.texto)
                if k == 0:
                    lienzo.arista(anterior, sid, etiqueta, punta, (0.5, 0),
                                  recta=sub.carril == paso.carril)
                else:
                    lienzo.arista(anterior, sid)
                anterior = sid
            if not abierta:
                continue
            if id_union and lista:
                lienzo.arista(anterior, id_union, salida=(0.5, 1), entrada=lado)
            elif id_union:
                lienzo.arista(anterior, id_union, etiqueta, punta, lado)
            elif lista:
                pendientes.append((anterior, "", None))
            else:
                pendientes.append((anterior, etiqueta, punta))
        if id_union:
            pendientes = [(id_union, "", None)]

    for texto, k, *opcion in d.notas:
        paso, x, yy, ancho, alto = colocados[k]
        alto_n = alto_nota(texto)
        lado_nota = opcion[0] if opcion else ("izquierda" if paso.carril == orden[-1] else "derecha")
        lado = x - ANCHO_NOTA - 26 if lado_nota == "izquierda" else x + ancho + 26
        nid = lienzo.vertice(ESTILO["nota"], lado, yy + alto / 2 - alto_n / 2, ANCHO_NOTA,
                             alto_n, texto)
        lienzo.arista(nid, ids[k], estilo="endArrow=none;dashed=1;html=1;strokeColor=#D69E2E;")

    return lienzo.xml(d.titulo)


# --- Enlace editable ---------------------------------------------------------------

def enlace_editable(xml: str) -> str:
    """Igual que «Exportar como URL» de draw.io: #R + deflate crudo en base64."""
    datos = urllib.parse.quote(xml, safe="~()*!.'")
    comprimido = zlib.compressobj(9, zlib.DEFLATED, -15)
    crudo = comprimido.compress(datos.encode()) + comprimido.flush()
    return "https://app.diagrams.net/#R" + urllib.parse.quote(base64.b64encode(crudo).decode(), safe="")


# --- Diagramas, en el orden del story map ------------------------------------------

DIAGRAMAS = [
    Diagrama(
        clave="hu-01",
        titulo="HU-01 · Crear mi cuenta con correo y contraseña",
        pasos=[
            inicio("Usuario"),
            accion("Usuario", "Abre Deshka por primera vez"),
            accion("App", "Muestra la bienvenida «Hola. Soy Deshka.»"),
            accion("Usuario", "Toca «Empezar»"),
            accion("App", "Muestra «Primero, tu cuenta.» con los campos de correo y contraseña"),
            accion("Usuario", "Escribe su correo y una contraseña de al menos 8 caracteres, y toca «Crear cuenta»"),
            accion("App", "Envía el registro con el idioma y la moneda del teléfono"),
            decision("API", "¿El correo ya está registrado?",
                     ("no", [accion("API", "Cifra la contraseña con Argon2 y crea el usuario sin verificar")]),
                     ("sí", [accion("API", "Rechaza el registro: el correo ya existe"), fin_flujo("API")])),
            accion("API", "Genera un código de 6 dígitos que vence en 15 minutos y lo envía al correo"),
            accion("App", "Muestra «Te mandé seis números.» con su teclado"),
            accion("Usuario", "Escribe el código de 6 dígitos y toca «Entrar»"),
            accion("App", "Envía el código"),
            decision("API", "¿El código es correcto y está vigente?",
                     ("sí", [accion("API", "Marca el correo como verificado y abre la sesión")]),
                     ("no", [accion("API", "Responde «Código incorrecto»"), fin_flujo("API")])),
            accion("App", "Guarda la sesión y abre la configuración inicial (HU-03)"),
            fin("App"),
        ],
        notas=[("En el MVP el envío se simula: el código queda en el registro del servidor", 9)],
    ),
    Diagrama(
        clave="hu-02",
        titulo="HU-02 · Entrar y salir de mi cuenta",
        pasos=[
            inicio("Usuario"),
            accion("Usuario", "Abre Deshka sin una sesión activa"),
            accion("App", "Muestra «Qué gusto verte de nuevo.» con correo y contraseña"),
            accion("Usuario", "Escribe su correo y su contraseña, y toca «Entrar»"),
            accion("App", "Envía el correo y la contraseña"),
            accion("API", "Busca el usuario y compara la contraseña con su hash Argon2"),
            decision("API", "¿Las credenciales son correctas?",
                     ("sí", [accion("API", "Emite un token de acceso (15 min) y uno de renovación (30 días)")]),
                     ("no", [accion("API", "Responde «Correo o contraseña incorrectos»"), fin_flujo("API")])),
            accion("App", "Guarda los tokens de forma segura, abre «Inicio» y pide sus datos"),
            accion("API", "Identifica a Ana por el token y arma su inicio"),
            accion("App", "Muestra el inicio con sus datos"),
            accion("Usuario", "Toca su avatar y luego «Cerrar sesión»"),
            accion("App", "Avisa a la API y borra los tokens del teléfono"),
            accion("API", "Revoca la sesión"),
            accion("App", "Vuelve a «Qué gusto verte de nuevo.»"),
            fin("App"),
        ],
        notas=[("Se revoca el token de renovación; el de acceso vence solo a los 15 minutos", 13)],
    ),
    Diagrama(
        clave="hu-03",
        titulo="HU-03 · Onboarding que siembra mis datos reales",
        pasos=[
            inicio("App"),
            accion("App", "Muestra «Ahora sí: ¿cómo te llamas?» (1 de 3)"),
            accion("Usuario", "Escribe «Ana» y toca «Mucho gusto»"),
            accion("App", "Envía el nombre a la API"),
            accion("API", "Guarda el nombre del usuario"),
            accion("App", "Muestra «Ana, ¿qué te trae por acá?» (2 de 3)"),
            accion("Usuario", "Elige «Quiero ahorrar y nunca puedo» y toca «Seguir»"),
            accion("App", "Envía el objetivo «ahorrar»"),
            accion("API", "Guarda el objetivo en las preferencias de Ana"),
            accion("App", "Muestra «¿Dónde tienes tu plata?» (3 de 3), con la moneda COP"),
            decision("Usuario", "¿Registra ya su cuenta principal?",
                     ("no", [accion("Usuario", "Toca «Lo hago después»")]),
                     ("sí", [accion("Usuario", "Elige «Un banco», la llama «Ahorros», escribe 1.200.000 y toca «Guardar y seguir»"),
                             accion("API", "Crea la cuenta «Ahorros» con saldo 1.200.000"),
                             accion("App", "Muestra la demostración «Cuéntame algo que hayas gastado hoy.»"),
                             accion("Usuario", "Toca «Después»")])),
            accion("App", "Marca la configuración como terminada"),
            accion("App", "Abre «Inicio»: «Cuéntame tu primer gasto» y $1.200.000 en sus cuentas"),
            fin("App"),
        ],
        notas=[("Cada respuesta se guarda al darla. Solo se guarda lo que Ana escribió: "
                "no se crean movimientos ni cuentas de ejemplo", 12),
               ("Si Ana cierra la app a mitad, al volver la app retoma en el primer paso que la "
                "API todavía no tiene", 1)],
    ),
    Diagrama(
        clave="hu-07",
        titulo="HU-07 · Registrar mis cuentas de banco y mi efectivo",
        pasos=[
            inicio("Usuario"),
            accion("Usuario", "En «Inicio» toca «En tus cuentas»"),
            accion("App", "Abre «Cuentas y tarjetas» y pide el resumen"),
            accion("API", "Lista las cuentas y tarjetas de Ana y calcula el saldo neto"),
            accion("Usuario", "Toca «Anotar otra cuenta»"),
            decision("App", "¿Plan Free y ya tiene 2 cuentas?",
                     ("no", [accion("App", "Abre la hoja de cuenta nueva, con «Débito» elegido")]),
                     ("sí", [accion("App", "Muestra «Tu plan Free llega hasta 2 cuentas»"), fin_flujo("App")])),
            accion("Usuario", "Deja «Débito», escribe 800.000 en «Saldo actual» y «Nómina» en «Nombre», y toca «Guardar»"),
            accion("App", "Envía la cuenta nueva"),
            accion("API", "Valida los datos y vuelve a revisar el límite del plan"),
            accion("API", "Crea la cuenta «Nómina» con saldo 800.000"),
            accion("App", "Cierra el formulario y actualiza las vistas de dinero"),
            accion("API", "Recalcula el saldo neto incluyendo «Nómina»"),
            accion("App", "Muestra «Nómina» con $800.000 y el neto actualizado"),
            fin("App"),
        ],
        notas=[("El saldo neto se calcula al leer; nunca se guarda (RN-14)", 12)],
    ),
    Diagrama(
        clave="hu-08",
        titulo="HU-08 · Registrar mi tarjeta de crédito",
        pasos=[
            inicio("Usuario"),
            accion("Usuario", "En «Cuentas y tarjetas» toca «Anotar una tarjeta»"),
            accion("App", "Abre el formulario «Nueva tarjeta»"),
            accion("Usuario", "Escribe 1.200.000 de «Deuda actual», «Visa», 5.000.000 de «Cupo», corte el 15 y pago el 5"),
            decision("App", "¿La deuda supera el cupo?",
                     ("no", [accion("App", "Habilita «Guardar»")]),
                     ("sí", [accion("App", "Muestra «La deuda no puede superar el cupo.»"), fin_flujo("App")])),
            accion("Usuario", "Toca «Guardar»"),
            accion("App", "Envía la tarjeta nueva"),
            accion("API", "Valida cupo, deuda, días de corte y pago, y el límite del plan"),
            accion("API", "Crea la tarjeta como una entidad propia, separada de las cuentas"),
            accion("App", "Actualiza las vistas de dinero"),
            accion("API", "Suma la deuda de las tarjetas y recalcula el saldo neto"),
            accion("App", "Muestra el grupo «Tarjetas»: Visa −$1.200.000, «Disponible $3.800.000», «24% del cupo» y «corte el 15 · pagas el 5»"),
            fin("App"),
        ],
        notas=[("La deuda de la tarjeta se resta del saldo neto (HU-09)", 11)],
    ),
    Diagrama(
        clave="hu-09",
        titulo="HU-09 · Ver un único saldo que ya descuenta lo que debo",
        pasos=[
            inicio("Usuario"),
            accion("Usuario", "Abre «Inicio»"),
            accion("App", "Pide el resumen de inicio con la fecha del teléfono"),
            accion("API", "Identifica a Ana por el token"),
            accion("API", "Suma las cuentas de débito y de efectivo"),
            accion("API", "Resta la deuda de las tarjetas: neto = débito + efectivo − deuda"),
            accion("API", "Arma el resto del inicio y responde"),
            decision("App", "¿Ana ya tiene movimientos?",
                     ("no", [accion("App", "Muestra arriba «Cuéntame tu primer gasto»")]),
                     ("sí", [accion("App", "Muestra arriba la cifra de su objetivo (HU-25)")])),
            accion("App", "Muestra «En tus cuentas» con el saldo neto y «2 cuentas · 1 tarjeta»"),
            fin("App"),
        ],
        notas=[("Escenario: 900.000 + 100.000 − 300.000 = 700.000", 5)],
    ),
    Diagrama(
        clave="hu-10",
        titulo="HU-10 · Clasificar mis gastos con el catálogo estándar",
        pasos=[
            inicio("Usuario"),
            accion("Usuario", "Toca el botón «+» y luego «Llenarlo a mano»"),
            accion("App", "Muestra el formulario manual en la pestaña «Gasto»"),
            accion("App", "Pide las categorías y las guarda en memoria"),
            accion("API", "Une las 15 categorías estándar con las propias de Ana"),
            accion("Usuario", "Toca «Categoría»"),
            decision("App", "¿Qué pestaña está activa?",
                     ("Gasto", [accion("App", "Muestra las 12 categorías de gasto")]),
                     ("Ingreso", [accion("App", "Muestra «Salario», «Freelance» y «Otro»")])),
            accion("Usuario", "Elige una categoría"),
            accion("App", "La muestra en el formulario"),
            fin("App"),
        ],
        notas=[("12 de gasto, como Mercado, Transporte u Hogar, y 3 de ingreso: Salario, "
                "Freelance y Otro", 3, "izquierda")],
    ),
    Diagrama(
        clave="hu-13",
        titulo="HU-13 · Registrar un gasto a mano",
        pasos=[
            inicio("Usuario"),
            accion("Usuario", "Toca el botón «+»"),
            accion("App", "Abre «¿Qué pasó?»"),
            accion("Usuario", "Toca «Llenarlo a mano»"),
            accion("App", "Muestra el formulario manual en la pestaña «Gasto»"),
            accion("Usuario", "Escribe 45.000 y «Mercado», deja la categoría Mercado, elige Nómina en «Sale de» y deja «Hoy»"),
            accion("Usuario", "Toca «Guardar gasto»"),
            decision("App", "¿El monto es mayor que cero?",
                     ("no", [accion("App", "No guarda y señala el monto: «Escribe un monto mayor que cero.»"),
                             fin_flujo("App")]),
                     ("sí", [accion("App", "Envía el gasto con una clave única, para no registrarlo dos veces")])),
            accion("API", "Toma el usuario del token y valida monto, fecha, fuente y categoría"),
            accion("API", "Guarda el movimiento"),
            decision("API", "¿La fuente es una tarjeta de crédito?",
                     ("no", [accion("API", "Baja el saldo de la cuenta")]),
                     ("sí", [accion("API", "Sube la deuda de la tarjeta")])),
            accion("API", "Confirma la transacción y responde con el movimiento"),
            accion("App", "Muestra «Gasto guardado» con la opción «Deshacer»"),
            accion("App", "Actualiza Inicio, Movimientos y saldos"),
            fin("App"),
        ],
        regiones=[("Transacción: todo o nada", 9, 10)],
        notas=[("Nómina pasa de 800.000 a 755.000 y el gasto del mes sube 45.000", 13)],
    ),
    Diagrama(
        clave="hu-14",
        titulo="HU-14 · Registrar el dinero que recibo",
        pasos=[
            inicio("Usuario"),
            accion("Usuario", "Toca el botón «+» y luego «Llenarlo a mano»"),
            accion("App", "Muestra el formulario manual en la pestaña «Gasto»"),
            accion("Usuario", "Toca la pestaña «Ingreso»"),
            accion("App", "Cambia «Sale de» por «Entra a», con solo cuentas, y muestra las categorías de ingreso"),
            accion("Usuario", "Escribe 3.000.000 y «Salario», deja la categoría Salario, elige Nómina en «Entra a» y toca «Guardar ingreso»"),
            accion("App", "Envía el ingreso con una clave única"),
            decision("API", "¿Esa clave ya se había usado?",
                     ("no", [accion("API", "Valida que llegue a una cuenta y que la categoría sea de ingreso"),
                             accion("API", "En una transacción guarda el ingreso y sube el saldo de Nómina")]),
                     ("sí", [accion("API", "Devuelve el ingreso que ya estaba guardado")])),
            accion("API", "Responde con el movimiento"),
            accion("App", "Muestra «Ingreso guardado» con «Deshacer» y actualiza las vistas"),
            fin("App"),
        ],
        notas=[("Nómina pasa de 200.000 a 3.200.000 y el ingreso del mes sube 3.000.000", 9),
               ("La categoría es opcional: si Ana no elige ninguna, se guarda y el historial lo "
                "muestra como «Ingreso sin categoría»", 4)],
    ),
    Diagrama(
        clave="hu-15",
        titulo="HU-15 · Mover dinero entre mis propias fuentes",
        pasos=[
            inicio("Usuario"),
            accion("Usuario", "Toca «+», luego «Llenarlo a mano» y la pestaña «Transferencia»"),
            accion("App", "Oculta «Categoría» y muestra «De» y «A»"),
            accion("Usuario", "Escribe 200.000 y elige Nómina en «De»"),
            accion("App", "En «A» ofrece todas las fuentes menos Nómina"),
            accion("Usuario", "Elige Ahorros en «A» y toca «Guardar transferencia»"),
            accion("App", "Envía la transferencia con una clave única"),
            accion("API", "Valida que el destino exista y sea distinto del origen"),
            accion("API", "Guarda el movimiento"),
            accion("API", "Baja el saldo de Nómina en 200.000"),
            decision("API", "¿El destino es una tarjeta de crédito?",
                     ("no", [accion("API", "Sube el saldo de Ahorros")]),
                     ("sí", [accion("API", "Baja la deuda de la tarjeta")])),
            accion("API", "Confirma la transacción y responde"),
            accion("App", "Muestra «Transferencia guardada» y la marca «Transferencia» y «No cuenta como gasto»"),
            fin("App"),
        ],
        regiones=[("Transacción: todo o nada", 8, 10)],
        notas=[("Nómina queda en 800.000 y Ahorros en 700.000; el gasto y el ingreso del mes no cambian", 12)],
    ),
    Diagrama(
        clave="hu-16",
        titulo="HU-16 · Usar y pagar la tarjeta sin que el gasto se cuente dos veces",
        pasos=[
            inicio("Usuario"),
            accion("Usuario", "Toca el botón «+» y luego «Llenarlo a mano»"),
            decision("Usuario", "¿Qué registra Ana?",
                     ("compra", [accion("Usuario", "En «Gasto» escribe 150.000 y elige la Visa en «Sale de»")]),
                     ("pago", [accion("Usuario", "En «Transferencia» escribe 500.000, «De» Nómina y «A» Visa")])),
            accion("Usuario", "Toca guardar"),
            accion("App", "Envía el movimiento con una clave única"),
            accion("API", "Valida y guarda el movimiento"),
            decision("API", "¿Es una transferencia?",
                     ("no", [accion("API", "Sube la deuda de la Visa en 150.000")]),
                     ("sí", [accion("API", "Baja el saldo de Nómina y la deuda de la Visa en 500.000")])),
            accion("API", "Confirma la transacción y responde"),
            accion("App", "Muestra el aviso y actualiza Inicio, Movimientos y saldos"),
            fin("App"),
        ],
        regiones=[("Transacción: todo o nada", 5, 6)],
        notas=[("La compra suma al gasto del mes y el pago no, porque es una transferencia: "
                "el gasto se cuenta una sola vez (RN-01)", 8)],
    ),
    Diagrama(
        clave="hu-23",
        titulo="HU-23 · Consultar mi historial con filtros",
        pasos=[
            inicio("Usuario"),
            accion("Usuario", "Toca la pestaña «Movimientos»"),
            accion("App", "Pide los movimientos del mes en curso"),
            accion("API", "Busca los movimientos de Ana del mes, del más reciente al más antiguo"),
            accion("App", "Los agrupa por día («Hoy», «Ayer») con el neto de cada día"),
            accion("Usuario", "Elige un filtro: «Mes», «Categoría», «Cuenta», «Tipo» o la búsqueda"),
            decision("App", "¿Cambió el mes?",
                     ("no", [accion("App", "Filtra en el teléfono la lista ya cargada")]),
                     ("sí", [accion("App", "Pide los movimientos del mes elegido"),
                             accion("API", "Busca y ordena los movimientos de ese mes")])),
            accion("App", "Muestra la lista filtrada con la opción «Limpiar»"),
            fin("App"),
        ],
    ),
    Diagrama(
        clave="hu-24",
        titulo="HU-24 · Editar y eliminar movimientos del historial",
        pasos=[
            inicio("Usuario"),
            accion("Usuario", "En «Movimientos» toca el gasto de 50.000"),
            accion("App", "Muestra «Movimiento» con sus datos"),
            decision("Usuario", "¿Qué quiere hacer Ana?",
                     ("editar", [accion("Usuario", "Cambia el monto a 30.000 y toca «Guardar cambios»")]),
                     ("eliminar", [accion("Usuario", "Toca «Borrar movimiento» y confirma «Sí, bórralo»")])),
            accion("App", "Envía el cambio o la eliminación"),
            accion("API", "Busca el movimiento de Ana y valida los datos"),
            accion("API", "Revierte el efecto anterior en la fuente"),
            decision("API", "¿Es una edición?",
                     ("sí", [accion("API", "Aplica el efecto nuevo y guarda el movimiento")]),
                     ("no", [accion("API", "Borra el movimiento")])),
            accion("API", "Confirma la transacción y responde"),
            accion("App", "Cierra el detalle y actualiza Inicio, Movimientos y saldos"),
            fin("App"),
        ],
        regiones=[("Transacción: todo o nada", 6, 7)],
        notas=[("Al editar, Nómina pasa de 750.000 a 770.000 y el gasto del mes se recalcula", 9)],
    ),
    Diagrama(
        clave="hu-25",
        titulo="HU-25 · Ver en el inicio cómo va mi mes",
        pasos=[
            inicio("Usuario"),
            accion("Usuario", "Abre «Inicio»"),
            accion("App", "Pide el resumen de inicio"),
            accion("API", "Lee el objetivo que Ana eligió en el onboarding"),
            accion("API", "Reúne saldo, gasto e ingresos del mes, techo, deudas y metas"),
            decision("API", "¿El objetivo es ahorrar?",
                     ("sí", [accion("API", "Elige su meta más cercana; sin meta, lo guardado en el mes; "
                                           "sin ingresos ni meta, la invitación a crear una")]),
                     ("no", [accion("API", "Elige el foco de su objetivo: sus deudas, o su gasto frente al mes anterior")])),
            decision("API", "¿Hay techo definido?",
                     ("no", [accion("API", "No envía ninguna cifra de techo ni de gasto diario"),
                             accion("App", "En su lugar ofrece «Ponerle un techo al mes»")]),
                     ("sí", [accion("API", "Agrega lo que queda del techo y la cifra por día")])),
            accion("API", "Responde el inicio con el foco elegido"),
            accion("App", "Muestra arriba la frase y la cifra del foco: «Llevas el 25% de Viaje»"),
            accion("App", "Muestra debajo «En tus cuentas», «Hoy» y «En qué se te va»"),
            fin("App"),
        ],
        notas=[("Sin movimientos, el foco es «Cuéntame tu primer gasto». Sin metas: «Ponle nombre a lo "
                "que estás ahorrando»; con ingresos: «Guardas el 99% de lo que te entra»", 8, "izquierda")],
    ),
    Diagrama(
        clave="hu-28",
        titulo="HU-28 · Ponerme un techo global de gasto",
        pasos=[
            inicio("Usuario"),
            accion("Usuario", "Toca la pestaña «Presupuestos»"),
            accion("App", "Pide el estado de los presupuestos"),
            accion("API", "Busca el techo global de Ana"),
            decision("App", "¿Ana ya tiene techo?",
                     ("no", [accion("App", "Muestra «Define tu presupuesto» y «Crear presupuesto mensual»")]),
                     ("sí", [accion("App", "Muestra el techo vigente y lo que le queda"), fin_flujo("App")])),
            accion("Usuario", "Toca «Crear presupuesto mensual»"),
            accion("App", "Abre la hoja «Tu techo de octubre»"),
            accion("Usuario", "Escribe 2.500.000 y toca «Guardar»"),
            accion("App", "Envía el techo global de 2.500.000"),
            decision("API", "¿Ya existe un techo global?",
                     ("no", [accion("API", "Guarda el techo, vigente desde este mes")]),
                     ("sí", [accion("API", "Lo rechaza: «Ya tienes un tope para eso»"), fin_flujo("API")])),
            accion("App", "Actualiza las vistas de dinero"),
            accion("App", "Muestra «Te queda», el porcentaje usado y el ritmo ideal; Inicio suma «Te queda · Presupuesto»"),
            fin("App"),
        ],
        notas=[("El techo sigue vigente mes a mes hasta que Ana lo cambie", 11)],
    ),
    Diagrama(
        clave="hu-29",
        titulo="HU-29 · Saber cuánto puedo gastar por día",
        pasos=[
            inicio("Usuario"),
            accion("Usuario", "Abre «Inicio»"),
            accion("App", "Pide el resumen de inicio con la fecha del teléfono"),
            accion("API", "Busca el techo global de Ana"),
            decision("API", "¿Hay techo definido?",
                     ("no", [accion("API", "Responde sin bloque de presupuesto"),
                             accion("App", "No muestra cifra diaria y ofrece «Ponerle un techo al mes»"),
                             fin_flujo("App")]),
                     ("sí", [accion("API", "Suma los gastos del mes y calcula lo que queda: techo − gastado")])),
            decision("API", "¿Todavía queda dinero?",
                     ("sí", [accion("API", "Divide lo que queda entre los días que faltan, contando hoy")]),
                     ("no", [accion("API", "No da cifra diaria: Ana ya pasó el techo")])),
            accion("App", "Muestra «Te queda · Presupuesto» y la cifra «por día» (o «Te pasaste»)"),
            fin("App"),
        ],
        notas=[("Escenario: (3.000.000 − 1.500.000) ÷ 10 días = 150.000 por día (RN-28)", 6)],
    ),
    Diagrama(
        clave="hu-47",
        titulo="HU-47 · Recibir el corte de mi mes",
        carriles=["Usuario", "App", "API", "Worker"],
        pasos=[
            inicio("Worker"),
            accion("Worker", "El día 1 a las 6:00 (UTC) arranca el job del mes anterior"),
            accion("Worker", "Recorre los usuarios uno por uno"),
            decision("Worker", "¿Ya tiene su Corte o hizo menos de 3 movimientos?",
                     ("no", [accion("Worker", "Reúne gasto por día, categorías, topes, metas y el mes anterior")]),
                     ("sí", [accion("Worker", "Salta a ese usuario"), fin_flujo("Worker")])),
            accion("Worker", "Arma solo las pantallas que tienen datos"),
            decision("Worker", "¿Respondió el modelo de lenguaje?",
                     ("sí", [accion("Worker", "Usa una frase del modelo por pantalla, sin cifras")]),
                     ("no", [accion("Worker", "Usa las frases de plantilla (RF-57)")])),
            accion("Worker", "Guarda El Corte una sola vez por usuario y mes"),
            accion("Usuario", "Más tarde abre «Inicio»"),
            accion("App", "Pide los cortes de Ana"),
            accion("API", "Devuelve los cortes de Ana, del más reciente al más antiguo"),
            accion("App", "Nombra el último en el enlace «El Corte de septiembre»"),
            accion("Usuario", "Toca «El Corte de septiembre»"),
            accion("App", "Lo marca como leído y lo reproduce como historias, pantalla por pantalla"),
            accion("Usuario", "Avanza con «Siguiente» y sale con «Salir»"),
            fin("Usuario"),
        ],
        notas=[("Pantallas posibles: portada, cifra del mes, categorías, dato curioso, ritmo, meta y jugada", 4)],
    ),
]


def main():
    pedidas = set(sys.argv[1:])
    filas = []
    for d in DIAGRAMAS:
        if pedidas and d.clave not in pedidas:
            continue
        xml = construir(d)
        ruta = CARPETA / f"{d.clave}.drawio"
        ruta.write_text(xml, encoding="utf-8")
        png = CARPETA / f"{d.clave}.png"
        if not Path(DRAWIO).exists():
            filas.append((d, enlace_editable(xml)))
            print("sin draw.io: solo", ruta.name, "(la imagen queda como estaba)")
            continue
        subprocess.run([DRAWIO, "--export", "--format", "png", "--scale", "2", "--border", "24",
                        "--output", str(png), str(ruta)], check=True, capture_output=True)
        # El SVG es el que va al PDF: es vectorial y se puede ampliar sin perder nitidez.
        subprocess.run([DRAWIO, "--export", "--format", "svg", "--border", "24",
                        "--output", str(png.with_suffix(".svg")), str(ruta)], check=True, capture_output=True)
        filas.append((d, enlace_editable(xml)))
        print("listo", d.clave, png.name)
    if not pedidas:
        lineas_md = ["# Diagramas de actividades · enlaces editables", "",
                     "Cada enlace abre el diagrama en el editor web de draw.io, sin cuenta.", ""]
        for d, url in filas:
            lineas_md += [f"## {d.titulo}", "", f"[Abrir en draw.io]({url})", ""]
        (CARPETA / "enlaces.md").write_text("\n".join(lineas_md), encoding="utf-8")


if __name__ == "__main__":
    main()
