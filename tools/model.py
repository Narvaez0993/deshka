"""Modelo de una historia de usuario del proyecto Deshka.

Fuente unica de verdad: de aqui salen tanto el catalogo en Markdown
(`historias/`) como el cuerpo de cada issue de GitHub.
"""

from dataclasses import dataclass, field


ACTIVIDADES = {
    "01": ("Empezar a usar Deshka", "El visitante se vuelve usuario y le cuenta al sistema qué quiere lograr."),
    "02": ("Configurar mi dinero", "El usuario declara de dónde sale y a dónde entra su plata."),
    "03": ("Registrar lo que pasa", "El usuario deja constancia de cada movimiento con el menor esfuerzo posible."),
    "04": ("Revisar mi día a día", "El usuario mira cómo va y mantiene el historial fiel a la realidad."),
    "05": ("Ponerme límites", "El usuario fija un número propio y se mide contra él."),
    "06": ("Cuidar mis compromisos", "El usuario no pierde de vista lo que se repite ni lo que debe."),
    "07": ("Ahorrar con propósito", "El usuario aparta plata para algo concreto y ve si va a llegar."),
    "08": ("Entender y decidir", "El agente le explica al usuario qué pasó y qué hacer."),
    "09": ("Administrar mi plan", "El usuario sabe qué consume, qué incluye su plan y cómo mejorarlo."),
}

RELEASES = {
    "R1": ("Release 1 · MVP", "Registrar y entender lo básico"),
    "R2": ("Release 2 · Sin fricción", "Captura asistida y control del gasto"),
    "R3": ("Release 3 · Agente", "El sistema trabaja por el usuario"),
}


@dataclass
class Historia:
    id: str                     # HU-01
    titulo: str
    actividad: str              # clave de ACTIVIDADES
    tarea: str                  # tarea del story map
    release: str                # clave de RELEASES
    rol: str
    quiero: str
    para: str
    ru: list                    # requisitos de usuario que satisface
    rf: list                    # requisitos funcionales que la especifican
    rn: list = field(default_factory=list)
    rnf: list = field(default_factory=list)
    escenarios: list = field(default_factory=list)   # [(titulo, [pasos])]
    nota: str = ""

    @property
    def encabezado(self):
        return f"{self.id} · {self.titulo}"

    @property
    def ancla(self):
        """Ancla tal como la genera GitHub para el encabezado de la historia."""
        out = []
        for ch in self.encabezado.lower():
            if ch.isalnum() or ch in "-_":
                out.append(ch)
            elif ch == " ":
                out.append("-")
        return "".join(out)

    def trazabilidad(self):
        partes = [", ".join(self.ru), ", ".join(self.rf)]
        if self.rn:
            partes.append(", ".join(self.rn))
        if self.rnf:
            partes.append(", ".join(self.rnf))
        return " · ".join(partes)

    def gherkin(self):
        lineas = []
        act_nombre = ACTIVIDADES[self.actividad][0]
        lineas.append(f"Característica: {act_nombre} — {self.titulo}")
        lineas.append("")
        for titulo, pasos in self.escenarios:
            lineas.append(f"  Escenario: {titulo}")
            for paso in pasos:
                lineas.append(f"    {paso}")
            lineas.append("")
        return "\n".join(lineas).rstrip()

    def cuerpo(self, con_encabezado=True):
        """Cuerpo Markdown de la historia (compartido por catalogo e issue)."""
        act_nombre = ACTIVIDADES[self.actividad][0]
        rel_nombre, rel_sub = RELEASES[self.release]
        p = []
        if con_encabezado:
            p.append(f"### {self.encabezado}")
            p.append("")
        p.append(f"> **Como** {self.rol},  ")
        p.append(f"> **quiero** {self.quiero},  ")
        p.append(f"> **para** {self.para}.")
        p.append("")
        p.append(f"| | |")
        p.append(f"|---|---|")
        p.append(f"| **Actividad** | {self.actividad} · {act_nombre} — *{self.tarea}* |")
        p.append(f"| **Release** | {rel_nombre} — {rel_sub} |")
        p.append(f"| **Requisitos de usuario** | {', '.join(self.ru) if self.ru else '—'} |")
        p.append(f"| **Requisitos funcionales** | {', '.join(self.rf) if self.rf else '— (brecha detectada en la matriz)'} |")
        p.append(f"| **Reglas de negocio** | {', '.join(self.rn) if self.rn else '—'} |")
        p.append(f"| **Requisitos no funcionales** | {', '.join(self.rnf) if self.rnf else '—'} |")
        p.append("")
        p.append("**Criterios de aceptación**")
        p.append("")
        p.append("```gherkin")
        p.append(self.gherkin())
        p.append("```")
        if self.nota:
            p.append("")
            p.append(f"> **Nota.** {self.nota}")
        return "\n".join(p)
