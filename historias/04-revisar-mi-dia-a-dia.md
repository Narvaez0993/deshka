# 04 · Revisar mi día a día

*El usuario mira cómo va y mantiene el historial fiel a la realidad.*

**Tareas del story map:** «Depurar el historial» · «Ver cómo voy»

| Historia | Título | Release | RF |
|---|---|---|---|
| `HU-23` | Consultar mi historial con filtros | Release 1 · MVP | RF-20 |
| `HU-24` | Editar y eliminar movimientos del historial | Release 1 · MVP | RF-19 |
| `HU-25` | Ver en el inicio cómo va mi mes | Release 1 · MVP | RF-28 |
| `HU-26` | Comparar mi gasto con el mes pasado | Release 2 · Sin fricción | RF-29 |
| `HU-27` | Saber cuánto ahorré este mes | Release 2 · Sin fricción | RF-30 |

---

### HU-23 · Consultar mi historial con filtros

> **Como** usuario,  
> **quiero** listar mis movimientos y filtrarlos por periodo, tipo, categoría y fuente,  
> **para** encontrar lo que busco sin recorrer toda la lista.

| | |
|---|---|
| **Actividad** | 04 · Revisar mi día a día — *Depurar el historial* |
| **Release** | Release 1 · MVP — Registrar y entender lo básico |
| **Requisitos de usuario** | RU-15 |
| **Requisitos funcionales** | RF-20 |
| **Reglas de negocio** | — |
| **Requisitos no funcionales** | RNF-02 |

**Criterios de aceptación**

```gherkin
Característica: Revisar mi día a día — Consultar mi historial con filtros

  Escenario: Listado del periodo en curso
    Dado que tengo movimientos registrados en varios meses
    Cuando abro el historial
    Entonces veo los movimientos del mes en curso ordenados del más reciente al más antiguo

  Escenario: Filtro combinado
    Dado que estoy en el historial
    Cuando filtro por tipo «gasto», categoría «Transporte» y fuente «Visa»
    Entonces solo veo los movimientos que cumplen las tres condiciones

  Escenario: Los movimientos especiales quedan señalados
    Dado que tengo una transferencia y un gasto originado en una suscripción
    Cuando los veo en el historial
    Entonces la transferencia aparece marcada como transferencia
    Y el gasto de la suscripción aparece marcado como recurrente

  Escenario: Rendimiento del listado
    Dado que mi cuenta tiene mil movimientos registrados
    Cuando abro el historial
    Entonces la lista se presenta en menos de dos segundos
```

---

### HU-24 · Editar y eliminar movimientos del historial

> **Como** usuario,  
> **quiero** corregir o borrar cualquier movimiento que registré,  
> **para** mantener el historial fiel a lo que realmente ocurrió.

| | |
|---|---|
| **Actividad** | 04 · Revisar mi día a día — *Depurar el historial* |
| **Release** | Release 1 · MVP — Registrar y entender lo básico |
| **Requisitos de usuario** | RU-15, RU-02 |
| **Requisitos funcionales** | RF-19 |
| **Reglas de negocio** | RN-27 |
| **Requisitos no funcionales** | RNF-09 |

**Criterios de aceptación**

```gherkin
Característica: Revisar mi día a día — Editar y eliminar movimientos del historial

  Escenario: Edición del monto de un gasto
    Dado que registré un gasto de 50.000 con cargo a «Nómina», que quedó en 750.000
    Cuando cambio el monto del gasto a 30.000
    Entonces «Nómina» queda en 770.000
    Y el gasto del mes se recalcula

  Escenario: Eliminación de un consumo con tarjeta
    Dado que registré un consumo de 150.000 con la tarjeta, cuya deuda quedó en 1.150.000
    Cuando elimino ese movimiento
    Entonces la deuda de la tarjeta vuelve a 1.000.000
    Y el gasto del mes disminuye en 150.000

  Escenario: Eliminación de un aporte a una meta
    Dado que aporté 100.000 a la meta «Viaje»
    Cuando elimino ese aporte
    Entonces lo ahorrado de la meta disminuye en 100.000
    Y el saldo de la cuenta de origen aumenta en 100.000

  Escenario: Confirmación antes de borrar
    Cuando pido eliminar un movimiento
    Entonces el sistema me pide confirmar
    Y solo entonces revierte sus efectos
```

---

### HU-25 · Ver en el inicio cómo va mi mes

> **Como** usuario,  
> **quiero** que la pantalla de inicio me muestre el ritmo de mi mes según el objetivo que declaré,  
> **para** entender mi situación de un vistazo y sin interpretar gráficas.

| | |
|---|---|
| **Actividad** | 04 · Revisar mi día a día — *Ver cómo voy* |
| **Release** | Release 1 · MVP — Registrar y entender lo básico |
| **Requisitos de usuario** | RU-20 |
| **Requisitos funcionales** | RF-28 |
| **Reglas de negocio** | RN-03, RN-04 |
| **Requisitos no funcionales** | RNF-02, RNF-12 |

**Criterios de aceptación**

```gherkin
Característica: Revisar mi día a día — Ver en el inicio cómo va mi mes

  Escenario: La vista se adapta al objetivo declarado
    Dado que declaré el objetivo «Ahorrar para algo»
    Cuando abro la pantalla de inicio
    Entonces la información principal corresponde al avance de mis metas

  Escenario: Nunca una figura sin datos
    Dado que no tengo ningún tope de gasto definido
    Cuando abro la pantalla de inicio
    Entonces no se presenta ninguna barra ni cifra de consumo de tope
    Y en su lugar se me ofrece definir uno

  Escenario: Ninguna cifra inventada
    Dado que no definí ningún tope
    Cuando abro la pantalla de inicio
    Entonces el sistema no presenta ningún gasto diario permitido derivado de mis ingresos
```

---

### HU-26 · Comparar mi gasto con el mes pasado

> **Como** usuario,  
> **quiero** comparar lo que llevo gastado con el mismo tramo del mes anterior,  
> **para** saber si voy mejor o peor que la última vez.

| | |
|---|---|
| **Actividad** | 04 · Revisar mi día a día — *Ver cómo voy* |
| **Release** | Release 2 · Sin fricción — Captura asistida y control del gasto |
| **Requisitos de usuario** | RU-08 |
| **Requisitos funcionales** | RF-29 |
| **Reglas de negocio** | RN-09 |
| **Requisitos no funcionales** | RNF-02 |

**Criterios de aceptación**

```gherkin
Característica: Revisar mi día a día — Comparar mi gasto con el mes pasado

  Escenario: Comparación sobre el mismo tramo de días
    Dado que hoy es 10 de mayo y llevo 400.000 gastados
    Y entre el 1 y el 10 de abril gasté 500.000
    Cuando abro la pantalla de inicio
    Entonces el sistema informa que voy 100.000 por debajo del mes anterior
    Y no compara contra el total de abril

  Escenario: Sin historial comparable
    Dado que es mi primer mes usando la aplicación
    Cuando abro la pantalla de inicio
    Entonces la comparación con el mes anterior se omite
    Y no se muestra una variación de cero por ciento
```

---

### HU-27 · Saber cuánto ahorré este mes

> **Como** usuario,  
> **quiero** ver la diferencia entre lo que recibí y lo que gasté en el mes,  
> **para** medir mi ahorro y no solamente mis salidas de dinero.

| | |
|---|---|
| **Actividad** | 04 · Revisar mi día a día — *Ver cómo voy* |
| **Release** | Release 2 · Sin fricción — Captura asistida y control del gasto |
| **Requisitos de usuario** | RU-03 |
| **Requisitos funcionales** | RF-30 |
| **Reglas de negocio** | RN-03 |
| **Requisitos no funcionales** | RNF-02 |

**Criterios de aceptación**

```gherkin
Característica: Revisar mi día a día — Saber cuánto ahorré este mes

  Escenario: Cálculo de la tasa de ahorro
    Dado que este mes registré ingresos por 3.000.000 y gastos por 2.100.000
    Cuando consulto mi tasa de ahorro
    Entonces el sistema informa 900.000 ahorrados, equivalentes al treinta por ciento de mis ingresos

  Escenario: Las transferencias no alteran el cálculo
    Dado que transferí 500.000 entre dos cuentas mías
    Cuando consulto mi tasa de ahorro
    Entonces el resultado no cambia por esa transferencia

  Escenario: Sin ingresos registrados
    Dado que no registré ningún ingreso este mes
    Cuando consulto mi tasa de ahorro
    Entonces el sistema no presenta un porcentaje
    Y me invita a registrar mis ingresos
```

---
