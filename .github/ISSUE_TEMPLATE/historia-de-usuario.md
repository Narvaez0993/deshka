---
name: Historia de usuario
about: Una necesidad del usuario con sus criterios de aceptación en Gherkin
title: "HU-XX · "
labels: historia-de-usuario
---

> **Como** <rol>,
> **quiero** <capacidad>,
> **para** <beneficio>.

| | |
|---|---|
| **Actividad** | NN · <actividad del story map> — *<tarea>* |
| **Release** | <Release 1 · MVP / Release 2 · Sin fricción / Release 3 · Agente> |
| **Requisitos de usuario** | RU-XX |
| **Requisitos funcionales** | RF-XX |
| **Reglas de negocio** | RN-XX |
| **Requisitos no funcionales** | RNF-XX |

**Criterios de aceptación**

```gherkin
Característica: <actividad> — <título de la historia>

  Escenario: <caso feliz>
    Dado que <contexto>
    Cuando <acción del usuario>
    Entonces <resultado observable>

  Escenario: <caso de borde o de error>
    Dado que <contexto>
    Cuando <acción del usuario>
    Entonces <resultado observable>
```
