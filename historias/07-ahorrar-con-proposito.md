# 07 · Ahorrar con propósito

*El usuario aparta plata para algo concreto y ve si va a llegar.*

**Tareas del story map:** «Crear la meta» · «Mover plata a la meta»

| Historia | Título | Release | RF |
|---|---|---|---|
| `HU-41` | Crear una meta de ahorro | Release 2 · Sin fricción | RF-39 |
| `HU-42` | Aportar y retirar dinero de mi meta | Release 2 · Sin fricción | RF-40 |
| `HU-43` | Ver mi progreso y si voy a llegar a tiempo | Release 2 · Sin fricción | RF-41 |
| `HU-44` | Cerrar y archivar una meta | Release 3 · Agente | RF-42 |

---

### HU-41 · Crear una meta de ahorro

> **Como** usuario,  
> **quiero** crear una meta con nombre, monto objetivo y fecha opcional,  
> **para** que ahorrar deje de ser una intención vaga.

| | |
|---|---|
| **Actividad** | 07 · Ahorrar con propósito — *Crear la meta* |
| **Release** | Release 2 · Sin fricción — Captura asistida y control del gasto |
| **Requisitos de usuario** | RU-12 |
| **Requisitos funcionales** | RF-39 |
| **Reglas de negocio** | RN-19 |
| **Requisitos no funcionales** | RNF-15 |

**Criterios de aceptación**

```gherkin
Característica: Ahorrar con propósito — Crear una meta de ahorro

  Escenario: Creación de una meta
    Cuando creo la meta «Viaje» por 4.000.000 con fecha objetivo el 15 de diciembre
    Entonces la meta aparece activa con 0 ahorrados

  Escenario: Meta sin fecha objetivo
    Cuando creo la meta «Fondo de emergencia» por 6.000.000 sin fecha
    Entonces el sistema la acepta
    Y no exige una fecha para operarla

  Escenario: Tope del plan gratuito
    Dado que estoy en el plan gratuito y ya tengo una meta activa
    Cuando intento crear otra
    Entonces el sistema impide la creación
    Y me informa el límite del plan
```

---

### HU-42 · Aportar y retirar dinero de mi meta

> **Como** usuario,  
> **quiero** apartar dinero para la meta y poder devolverlo cuando lo necesite,  
> **para** que el ahorro sea plata real y no una cifra declarada.

| | |
|---|---|
| **Actividad** | 07 · Ahorrar con propósito — *Mover plata a la meta* |
| **Release** | Release 2 · Sin fricción — Captura asistida y control del gasto |
| **Requisitos de usuario** | RU-12 |
| **Requisitos funcionales** | RF-40 |
| **Reglas de negocio** | RN-13, RN-14 |
| **Requisitos no funcionales** | RNF-09 |

**Criterios de aceptación**

```gherkin
Característica: Ahorrar con propósito — Aportar y retirar dinero de mi meta

  Escenario: Aporte a la meta
    Dado que «Nómina» tiene 1.000.000 y la meta «Viaje» tiene 0 ahorrados
    Cuando aporto 300.000 desde «Nómina»
    Entonces «Nómina» queda en 700.000 y la meta en 300.000
    Y el gasto del mes no cambia

  Escenario: Retiro desde la meta
    Dado que la meta «Viaje» tiene 300.000 apartados
    Cuando retiro 100.000 hacia «Nómina»
    Entonces la meta queda en 200.000 y «Nómina» aumenta en 100.000
    Y el ingreso del mes no cambia

  Escenario: Retiro superior a lo apartado
    Dado que la meta «Viaje» tiene 200.000 apartados
    Cuando intento retirar 250.000
    Entonces el sistema rechaza el retiro y me lo informa
```

---

### HU-43 · Ver mi progreso y si voy a llegar a tiempo

> **Como** usuario,  
> **quiero** ver cuánto llevo ahorrado y una estimación de cuándo cumpliré la meta,  
> **para** saber si mi ritmo alcanza o si tengo que aportar más.

| | |
|---|---|
| **Actividad** | 07 · Ahorrar con propósito — *Crear la meta* |
| **Release** | Release 2 · Sin fricción — Captura asistida y control del gasto |
| **Requisitos de usuario** | RU-12 |
| **Requisitos funcionales** | RF-41 |
| **Reglas de negocio** | RN-14, RN-23 |
| **Requisitos no funcionales** | RNF-02 |

**Criterios de aceptación**

```gherkin
Característica: Ahorrar con propósito — Ver mi progreso y si voy a llegar a tiempo

  Escenario: Lo ahorrado se deriva de los movimientos
    Dado que aporté 300.000 y retiré 100.000 de la meta «Viaje»
    Cuando consulto la meta
    Entonces lo ahorrado es 200.000
    Y esa cifra proviene de sus movimientos y no de un valor almacenado aparte

  Escenario: Aporte mensual necesario con fecha objetivo
    Dado que la meta «Viaje» es de 4.000.000, lleva 1.000.000 y vence en seis meses
    Cuando consulto su proyección
    Entonces el sistema informa que necesito aportar 500.000 mensuales

  Escenario: Fecha estimada sin fecha objetivo
    Dado que la meta «Fondo de emergencia» no tiene fecha y vengo aportando 200.000 al mes
    Cuando consulto su proyección
    Entonces el sistema estima la fecha de cumplimiento según ese ritmo

  Escenario: Sin historial de aportes
    Dado que la meta no tiene aportes todavía
    Cuando consulto su proyección
    Entonces el sistema no presenta una fecha estimada
```

---

### HU-44 · Cerrar y archivar una meta

> **Como** usuario,  
> **quiero** archivar o eliminar una meta cuando ya no la necesito,  
> **para** mantener mi lista limpia sin perder lo que ya logré.

| | |
|---|---|
| **Actividad** | 07 · Ahorrar con propósito — *Crear la meta* |
| **Release** | Release 3 · Agente — El sistema trabaja por el usuario |
| **Requisitos de usuario** | RU-12 |
| **Requisitos funcionales** | RF-42 |
| **Reglas de negocio** | RN-15 |
| **Requisitos no funcionales** | — |

**Criterios de aceptación**

```gherkin
Característica: Ahorrar con propósito — Cerrar y archivar una meta

  Escenario: Archivar una meta cumplida
    Dado que la meta «Viaje» no conserva dinero apartado
    Cuando la archivo
    Entonces sale de mis metas activas
    Y conservo su historial

  Escenario: Meta con dinero apartado
    Dado que la meta «Viaje» conserva 200.000 apartados
    Cuando intento archivarla o eliminarla
    Entonces el sistema lo impide
    Y me pide retirar primero el dinero

  Escenario: Archivar libera el cupo del plan gratuito
    Dado que estoy en el plan gratuito con una meta activa sin dinero apartado
    Cuando la archivo
    Entonces puedo crear una meta nueva
```

---
