# 05 · Ponerme límites

*El usuario fija un número propio y se mide contra él.*

**Tareas del story map:** «Definir el tope» · «Seguir el consumo»

| Historia | Título | Release | RF |
|---|---|---|---|
| `HU-28` | Ponerme un techo global de gasto | Release 1 · MVP | RF-23 |
| `HU-29` | Saber cuánto puedo gastar por día | Release 1 · MVP | RF-24 |
| `HU-30` | Ponerme topes por categoría | Release 2 · Sin fricción | RF-23 |
| `HU-31` | Que me avisen al ochenta por ciento y al pasarme | Release 2 · Sin fricción | RF-26 |
| `HU-32` | Ver cómo voy a cerrar el mes | Release 2 · Sin fricción | RF-25 |
| `HU-33` | Ver en qué comercios se me fue la plata | Release 3 · Agente | RF-27 |

---

### HU-28 · Ponerme un techo global de gasto

> **Como** usuario,  
> **quiero** fijar un tope general de gasto para el mes y ver cuánto llevo consumido,  
> **para** medirme contra un número que yo elegí.

| | |
|---|---|
| **Actividad** | 05 · Ponerme límites — *Definir el tope* |
| **Release** | Release 1 · MVP — Registrar y entender lo básico |
| **Requisitos de usuario** | RU-08 |
| **Requisitos funcionales** | RF-23 |
| **Reglas de negocio** | RN-04, RN-05, RN-06 |
| **Requisitos no funcionales** | RNF-15 |

**Criterios de aceptación**

```gherkin
Característica: Ponerme límites — Ponerme un techo global de gasto

  Escenario: Definición del techo global
    Dado que no tengo ningún tope definido
    Cuando fijo un techo global de 2.500.000 para el mes
    Entonces la pantalla de inicio muestra el consumo del techo

  Escenario: Todo gasto cuenta contra el techo
    Dado que tengo un techo global de 2.500.000 y llevo 1.000.000 gastados
    Cuando registro un gasto de 50.000 en una categoría sin tope propio
    Entonces el consumo del techo global pasa a 1.050.000

  Escenario: El tope sigue vigente el mes siguiente
    Dado que definí un techo global en mayo y no lo he modificado
    Cuando comienza junio
    Entonces el mismo techo rige para junio
    Y el consumo se reinicia en cero

  Escenario: Modificar el tope aplica al mes en curso
    Dado que llevo 1.000.000 consumidos de un techo de 2.500.000
    Cuando cambio el techo a 2.000.000
    Entonces el consumo del mes en curso pasa a medirse contra 2.000.000
```

---

### HU-29 · Saber cuánto puedo gastar por día

> **Como** usuario,  
> **quiero** ver cuánto puedo gastar diariamente en lo que resta del mes,  
> **para** no pasarme del tope que definí.

| | |
|---|---|
| **Actividad** | 05 · Ponerme límites — *Seguir el consumo* |
| **Release** | Release 1 · MVP — Registrar y entender lo básico |
| **Requisitos de usuario** | RU-09 |
| **Requisitos funcionales** | RF-24 |
| **Reglas de negocio** | RN-04, RN-07, RN-28 |
| **Requisitos no funcionales** | RNF-02 |

**Criterios de aceptación**

```gherkin
Característica: Ponerme límites — Saber cuánto puedo gastar por día

  Escenario: Cálculo del techo diario
    Dado que tengo un techo de 3.000.000, llevo 1.500.000 gastados y quedan diez días de mes contando hoy
    Cuando abro la pantalla de inicio
    Entonces el sistema informa 150.000 disponibles por día

  Escenario: Sin tope definido no hay cifra diaria
    Dado que no definí ningún tope
    Cuando abro la pantalla de inicio
    Entonces el sistema no presenta ninguna cifra de gasto diario
    Y me ofrece definir un tope

  Escenario: Tope superado
    Dado que gasté 3.200.000 de un techo de 3.000.000
    Cuando abro la pantalla de inicio
    Entonces el sistema informa un exceso de 200.000
    Y no presenta un disponible en cero ni una cifra diaria
```

---

### HU-30 · Ponerme topes por categoría

> **Como** usuario,  
> **quiero** fijar un tope para categorías concretas y ver el consumo de cada una,  
> **para** controlar los rubros que se me desbordan.

| | |
|---|---|
| **Actividad** | 05 · Ponerme límites — *Definir el tope* |
| **Release** | Release 2 · Sin fricción — Captura asistida y control del gasto |
| **Requisitos de usuario** | RU-08 |
| **Requisitos funcionales** | RF-23 |
| **Reglas de negocio** | RN-05, RN-19 |
| **Requisitos no funcionales** | RNF-12 |

**Criterios de aceptación**

```gherkin
Característica: Ponerme límites — Ponerme topes por categoría

  Escenario: Definición de un tope por categoría
    Dado que tengo un techo global de 2.500.000
    Cuando fijo un tope de 400.000 para «Mercado»
    Entonces veo el consumo de «Mercado» contra sus 400.000

  Escenario: Los topes por categoría no son acumulables
    Dado que tengo un techo global de 2.500.000 y topes de 400.000 y 300.000 en dos categorías
    Cuando registro un gasto de 100.000 en «Mercado»
    Entonces el consumo de «Mercado» aumenta en 100.000
    Y el consumo del techo global también aumenta en 100.000

  Escenario: Tope del plan gratuito
    Dado que estoy en el plan gratuito y ya tengo dos topes por categoría
    Cuando intento crear un tercero
    Entonces el sistema impide la creación
    Y me informa el límite del plan
```

---

### HU-31 · Que me avisen al ochenta por ciento y al pasarme

> **Como** usuario,  
> **quiero** recibir un aviso cuando un tope llega al ochenta por ciento y cuando lo supero,  
> **para** reaccionar antes de que sea tarde.

| | |
|---|---|
| **Actividad** | 05 · Ponerme límites — *Seguir el consumo* |
| **Release** | Release 2 · Sin fricción — Captura asistida y control del gasto |
| **Requisitos de usuario** | RU-08 |
| **Requisitos funcionales** | RF-26 |
| **Reglas de negocio** | RN-07 |
| **Requisitos no funcionales** | RNF-12 |

**Criterios de aceptación**

```gherkin
Característica: Ponerme límites — Que me avisen al ochenta por ciento y al pasarme

  Escenario: Aviso al ochenta por ciento
    Dado que tengo un tope de 400.000 en «Mercado» y llevo 300.000
    Cuando registro un gasto de 25.000 en esa categoría
    Entonces el sistema me avisa que consumí el ochenta por ciento del tope

  Escenario: Aviso al superar el tope
    Dado que tengo un tope de 400.000 en «Mercado» y llevo 390.000
    Cuando registro un gasto de 30.000 en esa categoría
    Entonces el sistema me avisa que superé el tope
    Y me informa un exceso de 20.000

  Escenario: El aviso no se repite por cada gasto
    Dado que ya recibí el aviso del ochenta por ciento de «Mercado» este mes
    Cuando registro otro gasto en esa categoría sin superar el tope
    Entonces el sistema no vuelve a emitir el mismo aviso
```

---

### HU-32 · Ver cómo voy a cerrar el mes

> **Como** usuario,  
> **quiero** ver una proyección de mi cierre del mes según el ritmo que llevo,  
> **para** corregir a tiempo si voy camino de pasarme.

| | |
|---|---|
| **Actividad** | 05 · Ponerme límites — *Seguir el consumo* |
| **Release** | Release 2 · Sin fricción — Captura asistida y control del gasto |
| **Requisitos de usuario** | RU-08 |
| **Requisitos funcionales** | RF-25 |
| **Reglas de negocio** | RN-08 |
| **Requisitos no funcionales** | RNF-02 |

**Criterios de aceptación**

```gherkin
Característica: Ponerme límites — Ver cómo voy a cerrar el mes

  Escenario: Proyección contrastada con el tope
    Dado que tengo un techo de 3.000.000, llevo 1.200.000 gastados y transcurrieron diez de treinta días
    Cuando abro la pantalla de inicio
    Entonces el sistema proyecta un cierre de 3.600.000
    Y advierte que superaría el techo en 600.000

  Escenario: Sin proyección al comenzar el mes
    Dado que hoy es el segundo día del mes
    Cuando abro la pantalla de inicio
    Entonces el sistema no emite proyección de cierre
    Y explica que aún no hay base suficiente
```

---

### HU-33 · Ver en qué comercios se me fue la plata

> **Como** usuario,  
> **quiero** ver, en cada categoría con tope, los tres comercios donde más gasté,  
> **para** saber qué concretamente está consumiendo mi tope.

| | |
|---|---|
| **Actividad** | 05 · Ponerme límites — *Seguir el consumo* |
| **Release** | Release 3 · Agente — El sistema trabaja por el usuario |
| **Requisitos de usuario** | RU-08 |
| **Requisitos funcionales** | RF-27 |
| **Reglas de negocio** | — |
| **Requisitos no funcionales** | RNF-02 |

**Criterios de aceptación**

```gherkin
Característica: Ponerme límites — Ver en qué comercios se me fue la plata

  Escenario: Los tres comercios de mayor gasto
    Dado que tengo un tope en «Mercado» con gastos en varios comercios
    Cuando abro el detalle de esa categoría
    Entonces veo los tres comercios de mayor gasto del periodo con su monto

  Escenario: Agrupación insensible a mayúsculas y espacios
    Dado que registré gastos con las descripciones «exito», «Éxito» y « EXITO »
    Cuando abro el detalle de la categoría
    Entonces los tres aparecen agrupados como un solo comercio

  Escenario: Categoría sin gastos
    Dado que una categoría con tope no tiene gastos en el periodo
    Cuando abro su detalle
    Entonces el sistema no presenta la lista de comercios
```

---
