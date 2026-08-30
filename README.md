# Deshka · Historias de usuario

**Coaching financiero personal, impulsado por IA.**
Deshka es un agente financiero personal en forma de aplicación móvil: el usuario registra lo que
gasta y lo que recibe hablando, escribiendo en lenguaje natural o fotografiando un recibo, y el
sistema lo organiza, lo contrasta con sus presupuestos, deudas y metas, y le explica qué está
pasando con su plata.

Este repositorio reúne los **artefactos públicos** del proyecto: el catálogo completo de historias
de usuario con criterios de aceptación en Gherkin, su story map, la trazabilidad hacia los requisitos
y el diagrama de clases de diseño. Corresponde a los **numerales 3 y 4 del Entregable #1** de Diseño
de Sistemas de Información.

> El código fuente de la aplicación (front y back) vive en repositorios privados. Aquí solo está la
> especificación funcional, que sí es pública.

## 📋 El roadmap

**→ [Deshka · Historias de usuario (GitHub Project)](https://github.com/users/Narvaez0993/projects/3)**

Un issue por historia, con vistas por **release**, por **actividad** del recorrido del usuario y por
**estado**. Es el tablero vivo del producto.

## Dónde está cada cosa

| | |
|---|---|
| 🗺️ [**Story map**](./docs/story-map.md) | El recorrido del usuario y el corte del MVP |
| 📖 [**Catálogo de historias**](./historias/README.md) | Las 54 historias con sus criterios de aceptación |
| 🔗 [**Trazabilidad**](./docs/trazabilidad.md) | RU y RF ↔ historias, y las brechas detectadas |
| 🧩 [**Diagrama de clases**](./docs/diagrama-de-clases.md) | El modelo de dominio completo, por módulos |
| 🛠️ [**Generador**](./tools/) | Fuente única desde la que se producen el catálogo y los issues |

## Cómo está organizado

El catálogo sigue exactamente la estructura del story map: **9 actividades** del recorrido del
usuario, cortadas en **3 releases**. Cada tarjeta del mapa es una historia y cada historia es un
issue.

| Actividad | Historias | |
|---|---|---|
| 01 · [Empezar a usar Deshka](./historias/01-empezar-a-usar-deshka.md) | 6 | El visitante se vuelve usuario y le cuenta al sistema qué quiere lograr |
| 02 · [Configurar mi dinero](./historias/02-configurar-mi-dinero.md) | 6 | Declara de dónde sale y a dónde entra su plata |
| 03 · [Registrar lo que pasa](./historias/03-registrar-lo-que-pasa.md) | 10 | Deja constancia de cada movimiento con el menor esfuerzo posible |
| 04 · [Revisar mi día a día](./historias/04-revisar-mi-dia-a-dia.md) | 5 | Mira cómo va y mantiene el historial fiel a la realidad |
| 05 · [Ponerme límites](./historias/05-ponerme-limites.md) | 6 | Fija un número propio y se mide contra él |
| 06 · [Cuidar mis compromisos](./historias/06-cuidar-mis-compromisos.md) | 7 | No pierde de vista lo que se repite ni lo que debe |
| 07 · [Ahorrar con propósito](./historias/07-ahorrar-con-proposito.md) | 4 | Aparta plata para algo concreto y ve si va a llegar |
| 08 · [Entender y decidir](./historias/08-entender-y-decidir.md) | 6 | El agente le explica qué pasó y qué hacer |
| 09 · [Administrar mi plan](./historias/09-administrar-mi-plan.md) | 4 | Sabe qué consume, qué incluye su plan y cómo mejorarlo |

| Release | Historias | Escenarios | Qué entrega |
|---|---|---|---|
| 🟢 **Release 1 · MVP** | 16 | 51 | Registrar y entender lo básico |
| 🟡 **Release 2 · Sin fricción** | 23 | 74 | Captura asistida y control del gasto |
| 🟣 **Release 3 · Agente** | 15 | 47 | El sistema trabaja por el usuario |
| | **54** | **172** | |

## Cómo se escribe una historia aquí

Todas siguen la misma estructura: narrativa, ficha de trazabilidad y criterios de aceptación en
Gherkin. Ningún escenario describe pantallas ni implementación; describe comportamiento observable.

```gherkin
Escenario: El pago de la tarjeta es transferencia y no gasto
  Dado que mi tarjeta tiene una deuda de 1.150.000 y «Nómina» tiene 900.000
  Cuando registro un pago de 500.000 a la tarjeta desde «Nómina»
  Entonces la deuda de la tarjeta pasa a 650.000
  Y «Nómina» queda en 400.000
  Y el gasto del mes no cambia
```

### Nomenclatura

| Prefijo | Qué identifica | Dónde vive |
|---|---|---|
| `HU-XX` | Historia de usuario | este repositorio |
| `RU-XX` | Requisito de usuario | Entregable #1, numeral 1.1 |
| `RF-XX` | Requisito funcional | Entregable #1, numeral 1.2 |
| `RNF-XX` | Requisito no funcional | Entregable #1, numeral 1.3 |
| `RN-XX` | Regla de negocio | Entregable #1, numeral 1.4 |

Cada historia declara los cuatro. La [trazabilidad](./docs/trazabilidad.md) recorre el camino
inverso y deja a la vista las dos brechas conocidas: `HU-05` (recuperar contraseña) y `HU-06`
(entrar con Google o Apple) todavía no tienen requisito funcional escrito, y por eso RU-18 figura
como cobertura parcial.

## Regenerar el catálogo

Las historias se definen una sola vez en `tools/data_*.py`; de ahí salen tanto los archivos de
`historias/` como el cuerpo de cada issue, de modo que el tablero y el documento nunca divergen.

```bash
python3 tools/generate.py
```

---

**Deshka** · Sebastián Mejía Narváez · Alexandra Guerrero Bocanegra
Diseño de Sistemas de Información · Instituto Tecnológico Metropolitano · Medellín, 2026
