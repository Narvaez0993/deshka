# 08 · Entender y decidir

*El agente le explica al usuario qué pasó y qué hacer.*

**Tareas del story map:** «Recibir avisos» · «Conversar con el agente» · «Recibir mis resúmenes» · «Aplicar lo que propone»

| Historia | Título | Release | RF |
|---|---|---|---|
| `HU-45` | Recibir avisos calculados sobre mi plata | Release 2 · Sin fricción | RF-43 |
| `HU-46` | Preguntarle al agente en mis palabras | Release 2 · Sin fricción | RF-44, RF-57 |
| `HU-47` | Recibir el corte de mi mes | Release 1 · MVP | RF-45, RF-57 |
| `HU-48` | Recibir mi revisión semanal | Release 3 · Agente | RF-46 |
| `HU-49` | Aplicar una jugada que el agente me sugirió | Release 3 · Agente | RF-47 |
| `HU-50` | Volver a leer lo que el agente ya me entregó | Release 3 · Agente | RF-48 |

---

### HU-45 · Recibir avisos calculados sobre mi plata

> **Como** usuario,  
> **quiero** recibir avisos derivados de mis propios datos, cada uno con algo que pueda hacer,  
> **para** enterarme de lo importante sin tener que ir a buscarlo.

| | |
|---|---|
| **Actividad** | 08 · Entender y decidir — *Recibir avisos* |
| **Release** | Release 2 · Sin fricción — Captura asistida y control del gasto |
| **Requisitos de usuario** | RU-13, RU-20 |
| **Requisitos funcionales** | RF-43 |
| **Reglas de negocio** | RN-03, RN-22 |
| **Requisitos no funcionales** | RNF-12, RNF-21 |

**Criterios de aceptación**

```gherkin
Característica: Entender y decidir — Recibir avisos calculados sobre mi plata

  Escenario: Aviso generado por una regla sobre mis datos
    Dado que tengo un cobro de «Streaming» previsto para dentro de dos días
    Cuando abro el feed
    Entonces veo un aviso de ese cobro próximo
    Y el aviso ofrece una acción que me lleva a la suscripción

  Escenario: Ningún aviso sobre datos no registrados
    Dado que no registré ningún movimiento este mes
    Cuando abro el feed
    Entonces no aparece ningún aviso que afirme conductas mías

  Escenario: Todo aviso tiene acción
    Dado que el feed tiene avisos
    Cuando reviso cada uno
    Entonces todos ejecutan una acción o navegan a la pantalla correspondiente
```

---

### HU-46 · Preguntarle al agente en mis palabras

> **Como** usuario,  
> **quiero** conversar con la aplicación y preguntarle por mis gastos, topes, metas, deudas y suscripciones,  
> **para** resolver dudas puntuales sin navegar entre pantallas.

| | |
|---|---|
| **Actividad** | 08 · Entender y decidir — *Conversar con el agente* |
| **Release** | Release 2 · Sin fricción — Captura asistida y control del gasto |
| **Requisitos de usuario** | RU-14 |
| **Requisitos funcionales** | RF-44, RF-57 |
| **Reglas de negocio** | RN-03, RN-19 |
| **Requisitos no funcionales** | RNF-03, RNF-23 |

**Criterios de aceptación**

```gherkin
Característica: Entender y decidir — Preguntarle al agente en mis palabras

  Escenario: Pregunta respondida con datos propios
    Dado que este mes gasté 320.000 en «Transporte»
    Cuando le pregunto «¿cuánto llevo en transporte?»
    Entonces el agente responde 320.000
    Y esa cifra proviene del cálculo del sistema y no de la redacción del modelo

  Escenario: Respuesta en mi idioma
    Dado que uso la aplicación en inglés
    Cuando le escribo al agente
    Entonces responde en inglés

  Escenario: Pregunta fuera de lo registrado
    Cuando le pregunto algo que mis datos no permiten responder
    Entonces el agente dice que no cuenta con esa información
    Y no inventa una cifra

  Escenario: Consumo de la cuota de mensajes
    Dado que estoy en el plan gratuito y llevo nueve mensajes en el mes
    Cuando envío otro mensaje al agente
    Entonces el contador pasa a diez

  Escenario: Falla del proveedor de inteligencia artificial
    Dado que el proveedor de inteligencia artificial no responde
    Cuando le escribo al agente
    Entonces el sistema me informa la indisponibilidad
    Y no presenta cifras inventadas ni una pantalla de error sin explicación
```

---

### HU-47 · Recibir el corte de mi mes

> **Como** usuario,  
> **quiero** recibir al comenzar el mes un resumen narrado del mes anterior,  
> **para** entender qué pasó con mi plata sin interpretar gráficas.

| | |
|---|---|
| **Actividad** | 08 · Entender y decidir — *Recibir mis resúmenes* |
| **Release** | Release 1 · MVP — Registrar y entender lo básico |
| **Requisitos de usuario** | RU-13 |
| **Requisitos funcionales** | RF-45, RF-57 |
| **Reglas de negocio** | RN-21, RN-24 |
| **Requisitos no funcionales** | RNF-10, RNF-21, RNF-23 |

**Criterios de aceptación**

```gherkin
Característica: Entender y decidir — Recibir el corte de mi mes

  Escenario: Composición del cierre mensual
    Dado que el mes anterior registré más de tres movimientos
    Cuando comienza el mes nuevo
    Entonces el sistema compone un resumen del mes anterior en secuencia de pantallas
    Y omite las pantallas que no tengan datos

  Escenario: Mes sin actividad suficiente
    Dado que el mes anterior registré dos movimientos
    Cuando comienza el mes nuevo
    Entonces no se genera cierre mensual

  Escenario: El cierre no consume mi cuota
    Dado que estoy en el plan gratuito
    Cuando recibo el cierre del mes
    Entonces mis contadores de uso no se incrementan

  Escenario: Falla del proveedor durante la composición
    Dado que el proveedor de inteligencia artificial falla al redactar el cierre
    Cuando el sistema entrega el resumen
    Entonces lo presenta con plantillas fijas sin cifras
    Y no omite la entrega ni muestra un error

  Escenario: Ejecución idempotente
    Dado que el proceso ya generó el cierre de abril
    Cuando vuelve a ejecutarse sobre ese periodo
    Entonces no se produce una segunda entrega
```

---

### HU-48 · Recibir mi revisión semanal

> **Como** usuario,  
> **quiero** recibir cada semana un diagnóstico, hasta tres acciones sugeridas y el resultado de las de la semana pasada,  
> **para** corregir el rumbo con algo concreto y saber si lo anterior sirvió.

| | |
|---|---|
| **Actividad** | 08 · Entender y decidir — *Recibir mis resúmenes* |
| **Release** | Release 3 · Agente — El sistema trabaja por el usuario |
| **Requisitos de usuario** | RU-13 |
| **Requisitos funcionales** | RF-46 |
| **Reglas de negocio** | RN-21, RN-22 |
| **Requisitos no funcionales** | RNF-10, RNF-21, RNF-23 |

**Criterios de aceptación**

```gherkin
Característica: Entender y decidir — Recibir mi revisión semanal

  Escenario: Entrega semanal
    Dado que cerró una semana con movimientos registrados
    Cuando el sistema genera la revisión
    Entonces recibo el diagnóstico de esa semana
    Y hasta tres acciones sugeridas

  Escenario: Rendición de cuentas de la semana anterior
    Dado que la semana pasada acepté la acción «tope de 200.000 en Comida fuera»
    Cuando recibo la revisión de esta semana
    Entonces incluye el resultado de esa acción

  Escenario: Semana sin movimientos
    Dado que no registré movimientos en la semana que cerró
    Cuando el sistema genera la revisión
    Entonces no presenta un diagnóstico con cifras
```

---

### HU-49 · Aplicar una jugada que el agente me sugirió

> **Como** usuario,  
> **quiero** aceptar una acción sugerida y que se convierta en un tope o en un aporte real,  
> **para** que el consejo se materialice sin que yo lo tenga que configurar.

| | |
|---|---|
| **Actividad** | 08 · Entender y decidir — *Aplicar lo que propone* |
| **Release** | Release 3 · Agente — El sistema trabaja por el usuario |
| **Requisitos de usuario** | RU-13 |
| **Requisitos funcionales** | RF-47 |
| **Reglas de negocio** | RN-22 |
| **Requisitos no funcionales** | RNF-12 |

**Criterios de aceptación**

```gherkin
Característica: Entender y decidir — Aplicar una jugada que el agente me sugirió

  Escenario: Acción que crea un tope
    Dado que el agente sugiere un tope de 200.000 en «Comida fuera»
    Cuando la aplico
    Entonces el tope queda creado con ese monto
    Y la acción aparece como aplicada

  Escenario: Acción que crea un aporte
    Dado que el agente sugiere aportar 150.000 a la meta «Viaje»
    Cuando la aplico
    Entonces se registra el aporte como transferencia real desde la cuenta que elegí

  Escenario: Nada se aplica sin mi confirmación
    Dado que el agente sugiere una acción
    Cuando no la acepto
    Entonces no se modifica ningún dato financiero

  Escenario: Aplicación fallida
    Dado que el agente sugiere un aporte de 150.000
    Y la cuenta de origen no tiene saldo suficiente
    Cuando intento aplicarla
    Entonces el sistema muestra el estado de falla y su motivo
    Y no registra el aporte
```

---

### HU-50 · Volver a leer lo que el agente ya me entregó

> **Como** usuario,  
> **quiero** que los cierres del mes y las revisiones queden archivados aunque los descarte del feed,  
> **para** poder releerlos cuando quiera.

| | |
|---|---|
| **Actividad** | 08 · Entender y decidir — *Recibir mis resúmenes* |
| **Release** | Release 3 · Agente — El sistema trabaja por el usuario |
| **Requisitos de usuario** | RU-13 |
| **Requisitos funcionales** | RF-48 |
| **Reglas de negocio** | — |
| **Requisitos no funcionales** | — |

**Criterios de aceptación**

```gherkin
Característica: Entender y decidir — Volver a leer lo que el agente ya me entregó

  Escenario: Descartar no elimina
    Dado que tengo el cierre de abril en el feed
    Cuando lo descarto
    Entonces desaparece del feed
    Y sigue disponible en el archivo de entregas

  Escenario: Consulta del archivo
    Dado que tengo varias entregas archivadas
    Cuando abro el archivo
    Entonces las veo ordenadas por periodo
    Y puedo abrir cualquiera completa
```

---
