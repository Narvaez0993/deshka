# 03 · Registrar lo que pasa

*El usuario deja constancia de cada movimiento con el menor esfuerzo posible.*

**Tareas del story map:** «Capturar el movimiento» · «Confirmar lo que entendió»

| Historia | Título | Release | RF |
|---|---|---|---|
| `HU-13` | Registrar un gasto a mano | Release 1 · MVP | RF-12 |
| `HU-14` | Registrar el dinero que recibo | Release 1 · MVP | RF-13 |
| `HU-15` | Mover dinero entre mis propias fuentes | Release 1 · MVP | RF-14 |
| `HU-16` | Usar y pagar la tarjeta sin que el gasto se cuente dos veces | Release 1 · MVP | RF-21 |
| `HU-17` | Registrar un gasto hablando | Release 2 · Sin fricción | RF-15 |
| `HU-18` | Registrar un gasto escribiendo en mis palabras | Release 2 · Sin fricción | RF-16 |
| `HU-19` | Revisar y corregir lo que el sistema entendió | Release 2 · Sin fricción | RF-18, RF-19 |
| `HU-20` | Recibir una categoría sugerida para cada movimiento | Release 2 · Sin fricción | RF-11 |
| `HU-21` | Registrar un gasto con la foto del recibo | Release 3 · Agente | RF-17 |
| `HU-22` | Registrar aunque no tenga conexión | Release 3 · Agente | RF-22 |

---

### HU-13 · Registrar un gasto a mano

> **Como** usuario,  
> **quiero** registrar un gasto indicando monto, descripción, fuente, categoría y fecha,  
> **para** dejar constancia exacta de lo que salió, sin depender de ninguna interpretación automática.

| | |
|---|---|
| **Actividad** | 03 · Registrar lo que pasa — *Capturar el movimiento* |
| **Release** | Release 1 · MVP — Registrar y entender lo básico |
| **Requisitos de usuario** | RU-01 |
| **Requisitos funcionales** | RF-12 |
| **Reglas de negocio** | RN-20 |
| **Requisitos no funcionales** | RNF-15 |

**Criterios de aceptación**

```gherkin
Característica: Registrar lo que pasa — Registrar un gasto a mano

  Escenario: Registro de un gasto con cargo a una cuenta
    Dado que tengo la cuenta «Nómina» con saldo 800.000
    Cuando registro un gasto de 45.000 con descripción «Mercado», categoría «Mercado», fuente «Nómina» y la fecha de hoy
    Entonces el movimiento queda guardado
    Y el saldo de «Nómina» pasa a 755.000
    Y el gasto del mes aumenta en 45.000

  Escenario: El registro manual no consume cuota
    Dado que estoy en el plan gratuito y agoté mis registros asistidos del mes
    Cuando registro un gasto a mano
    Entonces el sistema lo guarda con normalidad
    Y ningún contador de uso de inteligencia artificial se incrementa

  Escenario: Monto inválido
    Dado que estoy diligenciando un gasto
    Cuando indico un monto igual a cero o negativo
    Entonces el sistema rechaza el guardado
    Y señala el campo del monto
```

---

### HU-14 · Registrar el dinero que recibo

> **Como** usuario,  
> **quiero** registrar un ingreso con su monto, su fuente de destino y su fecha,  
> **para** saber cuánto ahorro y no solamente cuánto gasto.

| | |
|---|---|
| **Actividad** | 03 · Registrar lo que pasa — *Capturar el movimiento* |
| **Release** | Release 1 · MVP — Registrar y entender lo básico |
| **Requisitos de usuario** | RU-03 |
| **Requisitos funcionales** | RF-13 |
| **Reglas de negocio** | — |
| **Requisitos no funcionales** | RNF-15 |

**Criterios de aceptación**

```gherkin
Característica: Registrar lo que pasa — Registrar el dinero que recibo

  Escenario: Registro de un ingreso
    Dado que tengo la cuenta «Nómina» con saldo 200.000
    Cuando registro un ingreso de 3.000.000 con descripción «Salario» y destino «Nómina»
    Entonces el saldo de «Nómina» pasa a 3.200.000
    Y el ingreso del mes aumenta en 3.000.000

  Escenario: La categoría de ingreso es opcional
    Dado que estoy registrando un ingreso
    Cuando lo guardo sin elegir categoría
    Entonces el sistema lo acepta
    Y lo presenta en el historial como ingreso sin categoría

  Escenario: El ingreso no cuenta como gasto
    Dado que tengo un tope global de gasto definido
    Cuando registro un ingreso
    Entonces el consumo del tope no cambia
```

---

### HU-15 · Mover dinero entre mis propias fuentes

> **Como** usuario,  
> **quiero** registrar traslados entre dos fuentes mías,  
> **para** que mis saldos queden fieles sin que el traslado se cuente como gasto.

| | |
|---|---|
| **Actividad** | 03 · Registrar lo que pasa — *Capturar el movimiento* |
| **Release** | Release 1 · MVP — Registrar y entender lo básico |
| **Requisitos de usuario** | RU-05 |
| **Requisitos funcionales** | RF-14 |
| **Reglas de negocio** | RN-13 |
| **Requisitos no funcionales** | RNF-09 |

**Criterios de aceptación**

```gherkin
Característica: Registrar lo que pasa — Mover dinero entre mis propias fuentes

  Escenario: Transferencia entre dos cuentas
    Dado que tengo «Nómina» con 1.000.000 y «Ahorros» con 500.000
    Cuando transfiero 200.000 de «Nómina» a «Ahorros»
    Entonces «Nómina» queda en 800.000 y «Ahorros» en 700.000
    Y ni el gasto ni el ingreso del mes cambian

  Escenario: La transferencia es atómica
    Dado que una transferencia está en curso
    Cuando falla la actualización de la fuente de destino
    Entonces el sistema no descuenta la fuente de origen
    Y ningún saldo queda modificado a medias

  Escenario: Origen y destino no pueden ser la misma fuente
    Dado que estoy registrando una transferencia
    Cuando elijo la misma fuente como origen y como destino
    Entonces el sistema rechaza la operación
```

---

### HU-16 · Usar y pagar la tarjeta sin que el gasto se cuente dos veces

> **Como** usuario con tarjeta de crédito,  
> **quiero** que el consumo con tarjeta sea gasto y que el pago de la tarjeta no vuelva a serlo,  
> **para** que mi presupuesto no se descuadre.

| | |
|---|---|
| **Actividad** | 03 · Registrar lo que pasa — *Capturar el movimiento* |
| **Release** | Release 1 · MVP — Registrar y entender lo básico |
| **Requisitos de usuario** | RU-06 |
| **Requisitos funcionales** | RF-21 |
| **Reglas de negocio** | RN-01, RN-02 |
| **Requisitos no funcionales** | RNF-09 |

**Criterios de aceptación**

```gherkin
Característica: Registrar lo que pasa — Usar y pagar la tarjeta sin que el gasto se cuente dos veces

  Escenario: El consumo con tarjeta es gasto y aumenta la deuda
    Dado que mi tarjeta tiene una deuda de 1.000.000
    Cuando registro un gasto de 150.000 con cargo a la tarjeta
    Entonces el gasto del mes aumenta en 150.000
    Y la deuda de la tarjeta pasa a 1.150.000
    Y ningún saldo de mis cuentas cambia

  Escenario: El pago de la tarjeta es transferencia y no gasto
    Dado que mi tarjeta tiene una deuda de 1.150.000 y «Nómina» tiene 900.000
    Cuando registro un pago de 500.000 a la tarjeta desde «Nómina»
    Entonces la deuda de la tarjeta pasa a 650.000
    Y «Nómina» queda en 400.000
    Y el gasto del mes no cambia

  Escenario: Compra a cuotas
    Dado que mi tarjeta tiene una deuda de 0
    Cuando registro una compra de 1.200.000 a doce cuotas
    Entonces la deuda de la tarjeta aumenta en 1.200.000 en el momento de la compra
    Y el gasto del mes aumenta en 1.200.000
    Y cada cuota que pague después se registra como transferencia y no como gasto nuevo

  Escenario: La operación es atómica
    Dado que registro un consumo con tarjeta
    Cuando falla la actualización de la deuda
    Entonces el movimiento no queda guardado
    Y ni el gasto del mes ni la deuda quedan modificados
```

---

### HU-17 · Registrar un gasto hablando

> **Como** usuario,  
> **quiero** dictar lo que gasté y que el sistema arme el movimiento,  
> **para** no abandonar el registro por el esfuerzo que exige la digitación.

| | |
|---|---|
| **Actividad** | 03 · Registrar lo que pasa — *Capturar el movimiento* |
| **Release** | Release 2 · Sin fricción — Captura asistida y control del gasto |
| **Requisitos de usuario** | RU-01 |
| **Requisitos funcionales** | RF-15 |
| **Reglas de negocio** | RN-19 |
| **Requisitos no funcionales** | RNF-01, RNF-11, RNF-23 |

**Criterios de aceptación**

```gherkin
Característica: Registrar lo que pasa — Registrar un gasto hablando

  Escenario: Dictado interpretado
    Dado que tengo la cuenta «Nómina» y la tarjeta «Visa»
    Cuando dicto «gasté treinta mil en el almuerzo con la Visa»
    Entonces el sistema propone un gasto de 30.000 con descripción «almuerzo», categoría «Comida fuera», fuente «Visa» y la fecha de hoy
    Y me presenta la pantalla de confirmación en menos de cinco segundos

  Escenario: El dictado consume un registro asistido
    Dado que llevo diez registros asistidos consumidos en el mes
    Cuando guardo un movimiento capturado por voz
    Entonces el contador de registros asistidos pasa a once

  Escenario: Dictado incomprensible
    Dado que dicto una frase sin monto reconocible
    Cuando el sistema termina de interpretarla
    Entonces me presenta el formulario manual con lo que sí pudo derivar
    Y no guarda ningún movimiento por su cuenta
```

---

### HU-18 · Registrar un gasto escribiendo en mis palabras

> **Como** usuario,  
> **quiero** escribir una frase en lenguaje natural y que el sistema derive los campos del movimiento,  
> **para** registrar sin diligenciar un formulario campo por campo.

| | |
|---|---|
| **Actividad** | 03 · Registrar lo que pasa — *Capturar el movimiento* |
| **Release** | Release 2 · Sin fricción — Captura asistida y control del gasto |
| **Requisitos de usuario** | RU-01 |
| **Requisitos funcionales** | RF-16 |
| **Reglas de negocio** | RN-19 |
| **Requisitos no funcionales** | RNF-11, RNF-23 |

**Criterios de aceptación**

```gherkin
Característica: Registrar lo que pasa — Registrar un gasto escribiendo en mis palabras

  Escenario: Frase interpretada
    Cuando escribo «12.000 de taxi ayer»
    Entonces el sistema propone un gasto de 12.000 con descripción «taxi», categoría «Transporte» y la fecha de ayer

  Escenario: Frase que describe un ingreso
    Cuando escribo «me pagaron 3 millones del salario»
    Entonces el sistema propone un ingreso de 3.000.000 y no un gasto

  Escenario: Fuente no mencionada
    Dado que tengo más de una fuente de dinero
    Cuando escribo una frase que no menciona con qué pagué
    Entonces el sistema deja la fuente sin preseleccionar
    Y me pide elegirla antes de guardar
```

---

### HU-19 · Revisar y corregir lo que el sistema entendió

> **Como** usuario,  
> **quiero** ver los campos interpretados y poder editarlos antes de guardar,  
> **para** confiar en la información aunque la interpretación automática se equivoque.

| | |
|---|---|
| **Actividad** | 03 · Registrar lo que pasa — *Confirmar lo que entendió* |
| **Release** | Release 2 · Sin fricción — Captura asistida y control del gasto |
| **Requisitos de usuario** | RU-02 |
| **Requisitos funcionales** | RF-18, RF-19 |
| **Reglas de negocio** | RN-22 |
| **Requisitos no funcionales** | RNF-11, RNF-12 |

**Criterios de aceptación**

```gherkin
Característica: Registrar lo que pasa — Revisar y corregir lo que el sistema entendió

  Escenario: Confirmación antes de guardar
    Dado que capturé un movimiento por voz, por texto o por foto
    Cuando el sistema termina de interpretarlo
    Entonces me muestra monto, descripción, categoría, fuente y fecha en campos editables
    Y nada queda guardado hasta que confirmo

  Escenario: Corrección de un campo interpretado
    Dado que el sistema propuso la categoría «Mercado»
    Cuando la cambio a «Entretenimiento» y confirmo
    Entonces el movimiento se guarda con la categoría que yo elegí

  Escenario: Corrección después de guardar
    Dado que guardé un movimiento con un monto equivocado
    Cuando lo edito e indico el monto correcto
    Entonces el sistema revierte el efecto anterior sobre los saldos y aplica el nuevo

  Escenario: Descartar la interpretación
    Dado que el sistema entendió algo que no corresponde
    Cuando descarto la propuesta
    Entonces no se guarda ningún movimiento
```

---

### HU-20 · Recibir una categoría sugerida para cada movimiento

> **Como** usuario,  
> **quiero** que el sistema proponga la categoría de lo que registro,  
> **para** no tener que clasificar cada movimiento a mano.

| | |
|---|---|
| **Actividad** | 03 · Registrar lo que pasa — *Confirmar lo que entendió* |
| **Release** | Release 2 · Sin fricción — Captura asistida y control del gasto |
| **Requisitos de usuario** | RU-07 |
| **Requisitos funcionales** | RF-11 |
| **Reglas de negocio** | RN-20 |
| **Requisitos no funcionales** | RNF-11 |

**Criterios de aceptación**

```gherkin
Característica: Registrar lo que pasa — Recibir una categoría sugerida para cada movimiento

  Escenario: Sugerencia sobre una descripción conocida
    Cuando registro un movimiento con descripción «Éxito»
    Entonces el sistema propone la categoría «Mercado»
    Y la propuesta queda editable

  Escenario: La clasificación no consume cuota
    Dado que agoté mis registros asistidos del mes
    Cuando registro un gasto a mano
    Entonces el sistema igual me propone una categoría
    Y ningún contador de uso se incrementa

  Escenario: Sin categoría clara
    Cuando registro un movimiento cuya descripción no permite deducir la categoría
    Entonces el sistema deja el campo sin preseleccionar
    Y no elige una categoría al azar
```

---

### HU-21 · Registrar un gasto con la foto del recibo

> **Como** usuario,  
> **quiero** fotografiar un recibo y que el sistema extraiga los datos del movimiento,  
> **para** registrar lo que compré sin transcribir el papel.

| | |
|---|---|
| **Actividad** | 03 · Registrar lo que pasa — *Capturar el movimiento* |
| **Release** | Release 3 · Agente — El sistema trabaja por el usuario |
| **Requisitos de usuario** | RU-01 |
| **Requisitos funcionales** | RF-17 |
| **Reglas de negocio** | RN-19 |
| **Requisitos no funcionales** | RNF-01, RNF-11, RNF-23 |

**Criterios de aceptación**

```gherkin
Característica: Registrar lo que pasa — Registrar un gasto con la foto del recibo

  Escenario: Recibo legible
    Cuando fotografío un recibo con total 87.500 del comercio «Farmatodo»
    Entonces el sistema propone un gasto de 87.500 con descripción «Farmatodo» y categoría «Salud»
    Y conserva la imagen asociada al movimiento

  Escenario: Recibo ilegible
    Cuando fotografío un recibo del que no puede extraerse el total
    Entonces el sistema me presenta el formulario con los campos que sí pudo derivar
    Y me pide completar el monto

  Escenario: La imagen queda disponible en el historial
    Dado que guardé un movimiento capturado por foto
    Cuando lo abro desde el historial
    Entonces puedo ver la imagen del recibo
```

---

### HU-22 · Registrar aunque no tenga conexión

> **Como** usuario sin conexión a internet,  
> **quiero** registrar un movimiento y que se sincronice cuando vuelva la señal,  
> **para** no perder el registro justo cuando estoy fuera de cobertura.

| | |
|---|---|
| **Actividad** | 03 · Registrar lo que pasa — *Capturar el movimiento* |
| **Release** | Release 3 · Agente — El sistema trabaja por el usuario |
| **Requisitos de usuario** | RU-17 |
| **Requisitos funcionales** | RF-22 |
| **Reglas de negocio** | RN-30 |
| **Requisitos no funcionales** | RNF-16, RNF-24 |

**Criterios de aceptación**

```gherkin
Característica: Registrar lo que pasa — Registrar aunque no tenga conexión

  Escenario: Registro sin conexión
    Dado que mi dispositivo no tiene conexión
    Cuando registro un gasto de 20.000
    Entonces el movimiento queda guardado en el dispositivo
    Y el historial lo muestra señalado como pendiente de sincronizar

  Escenario: Sincronización al recuperar la conexión
    Dado que tengo dos movimientos pendientes de sincronizar
    Cuando el dispositivo recupera la conexión
    Entonces el sistema los envía automáticamente
    Y la marca de pendiente desaparece

  Escenario: Los saldos locales reflejan lo pendiente
    Dado que registré un gasto sin conexión
    Cuando consulto mi saldo neto en el dispositivo
    Entonces el gasto ya está descontado
```

> **Nota.** RNF-24 fija cuándo y cómo se sincroniza lo registrado sin conexión, y RN-30 resuelve el conflicto entre una edición local y una remota del mismo movimiento: prevalece la última edición confirmada por el usuario y la otra queda en su historial.

---
