# 06 · Cuidar mis compromisos

*El usuario no pierde de vista lo que se repite ni lo que debe.*

**Tareas del story map:** «Suscripciones» · «Deudas con personas»

| Historia | Título | Release | RF |
|---|---|---|---|
| `HU-34` | Registrar mis suscripciones | Release 2 · Sin fricción | RF-31 |
| `HU-35` | Confirmar el cobro del día | Release 2 · Sin fricción | RF-32 |
| `HU-36` | Que el cobro se liquide solo si no respondo | Release 2 · Sin fricción | RF-33 |
| `HU-37` | Llevar cuentas de lo que debo y de lo que me deben | Release 2 · Sin fricción | RF-35, RF-36 |
| `HU-38` | Que el sistema detecte mis cargos repetidos | Release 3 · Agente | RF-34 |
| `HU-39` | Dividir un gasto compartido | Release 3 · Agente | RF-37 |
| `HU-40` | Recordarle la deuda a la otra persona | Release 3 · Agente | RF-38 |

---

### HU-34 · Registrar mis suscripciones

> **Como** usuario,  
> **quiero** crear, editar, pausar y eliminar mis cobros recurrentes,  
> **para** que ningún cobro me tome por sorpresa.

| | |
|---|---|
| **Actividad** | 06 · Cuidar mis compromisos — *Suscripciones* |
| **Release** | Release 2 · Sin fricción — Captura asistida y control del gasto |
| **Requisitos de usuario** | RU-10 |
| **Requisitos funcionales** | RF-31 |
| **Reglas de negocio** | RN-16, RN-17 |
| **Requisitos no funcionales** | RNF-15 |

**Criterios de aceptación**

```gherkin
Característica: Cuidar mis compromisos — Registrar mis suscripciones

  Escenario: Creación de una suscripción
    Dado que estoy en la sección de suscripciones
    Cuando registro «Streaming» por 26.900 mensuales con cobro el día 8
    Entonces la suscripción aparece en mi lista con su próximo cobro
    Y ningún saldo de mis fuentes cambia

  Escenario: La suscripción no genera cobros anteriores a su registro
    Dado que hoy es 20 de mayo
    Cuando registro una suscripción con cobro el día 8
    Entonces el primer cobro previsto es el 8 de junio
    Y no se crea ningún cobro del 8 de mayo

  Escenario: Pausar una suscripción
    Dado que tengo la suscripción «Streaming» activa
    Cuando la pauso
    Entonces deja de generar cobros pendientes
    Y conserva su historial
```

---

### HU-35 · Confirmar el cobro del día

> **Como** usuario,  
> **quiero** que el sistema me pregunte el día del cobro si se realizó, si lo omito o si pauso la suscripción,  
> **para** que solo se registre el dinero que de verdad salió.

| | |
|---|---|
| **Actividad** | 06 · Cuidar mis compromisos — *Suscripciones* |
| **Release** | Release 2 · Sin fricción — Captura asistida y control del gasto |
| **Requisitos de usuario** | RU-10 |
| **Requisitos funcionales** | RF-32 |
| **Reglas de negocio** | RN-16 |
| **Requisitos no funcionales** | RNF-10 |

**Criterios de aceptación**

```gherkin
Característica: Cuidar mis compromisos — Confirmar el cobro del día

  Escenario: Apertura del cobro pendiente
    Dado que tengo la suscripción «Streaming» con cobro el día 8
    Cuando llega el día 8
    Entonces el sistema abre un cobro pendiente
    Y me ofrece confirmarlo, omitirlo o pausar la suscripción

  Escenario: Confirmación del cobro
    Dado que tengo un cobro pendiente de 26.900
    Cuando lo confirmo
    Entonces se registra un gasto de 26.900 en la fuente asociada
    Y el cobro pendiente se cierra

  Escenario: Omisión del cobro
    Dado que tengo un cobro pendiente de 26.900
    Cuando lo omito
    Entonces no se registra ningún gasto
    Y la suscripción conserva su próximo cobro para el periodo siguiente

  Escenario: Ejecución idempotente
    Dado que el proceso automático ya abrió el cobro del día 8
    Cuando el proceso vuelve a ejecutarse sobre ese mismo día
    Entonces no se crea un segundo cobro pendiente
```

---

### HU-36 · Que el cobro se liquide solo si no respondo

> **Como** usuario,  
> **quiero** que el cobro pendiente se registre automáticamente si no respondo en tres horas, y poder revertirlo,  
> **para** que mi historial no dependa de que yo esté pendiente del teléfono.

| | |
|---|---|
| **Actividad** | 06 · Cuidar mis compromisos — *Suscripciones* |
| **Release** | Release 2 · Sin fricción — Captura asistida y control del gasto |
| **Requisitos de usuario** | RU-10 |
| **Requisitos funcionales** | RF-33 |
| **Reglas de negocio** | RN-16 |
| **Requisitos no funcionales** | RNF-10 |

**Criterios de aceptación**

```gherkin
Característica: Cuidar mis compromisos — Que el cobro se liquide solo si no respondo

  Escenario: Liquidación automática
    Dado que tengo un cobro pendiente de 26.900 abierto hace tres horas
    Cuando no he respondido
    Entonces el sistema registra el gasto
    Y lo marca como registrado automáticamente

  Escenario: Reversión de un cobro automático
    Dado que el sistema liquidó automáticamente un cobro de 26.900
    Cuando lo revierto
    Entonces el gasto se elimina
    Y el saldo de la fuente vuelve a su valor anterior

  Escenario: Respuesta dentro de la ventana
    Dado que tengo un cobro pendiente abierto hace una hora
    Cuando lo omito
    Entonces el sistema no lo liquida automáticamente después
```

---

### HU-37 · Llevar cuentas de lo que debo y de lo que me deben

> **Como** usuario,  
> **quiero** registrar deudas con personas y sus abonos parciales,  
> **para** no perder la cuenta de préstamos y gastos compartidos.

| | |
|---|---|
| **Actividad** | 06 · Cuidar mis compromisos — *Deudas con personas* |
| **Release** | Release 2 · Sin fricción — Captura asistida y control del gasto |
| **Requisitos de usuario** | RU-11 |
| **Requisitos funcionales** | RF-35, RF-36 |
| **Reglas de negocio** | RN-10, RN-12 |
| **Requisitos no funcionales** | RNF-09 |

**Criterios de aceptación**

```gherkin
Característica: Cuidar mis compromisos — Llevar cuentas de lo que debo y de lo que me deben

  Escenario: Registro de una deuda a mi favor
    Cuando registro que «Camilo» me debe 120.000 por «Entradas del concierto» con vencimiento el 30 de mayo
    Entonces la deuda aparece con saldo pendiente 120.000
    Y ningún saldo de mis fuentes cambia

  Escenario: Abono parcial
    Dado que «Camilo» me debe 120.000
    Cuando registro un abono de 50.000
    Entonces el saldo pendiente pasa a 70.000
    Y la deuda sigue en estado pendiente

  Escenario: Abono que salda la deuda
    Dado que «Camilo» me debe 70.000
    Cuando registro un abono de 70.000
    Entonces el saldo pendiente pasa a cero
    Y la deuda queda en estado saldada

  Escenario: Abono superior al saldo pendiente
    Dado que «Camilo» me debe 70.000
    Cuando intento registrar un abono de 100.000
    Entonces el sistema rechaza el abono y me lo informa
    Y no lo ajusta automáticamente a 70.000

  Escenario: Deshacer el último abono
    Dado que registré por error un abono de 50.000
    Cuando deshago el último abono
    Entonces el saldo pendiente vuelve a su valor anterior
```

---

### HU-38 · Que el sistema detecte mis cargos repetidos

> **Como** usuario,  
> **quiero** que el sistema identifique gastos que se repiten y me proponga convertirlos en suscripción,  
> **para** no tener que acordarme de registrarlos yo.

| | |
|---|---|
| **Actividad** | 06 · Cuidar mis compromisos — *Suscripciones* |
| **Release** | Release 3 · Agente — El sistema trabaja por el usuario |
| **Requisitos de usuario** | RU-10 |
| **Requisitos funcionales** | RF-34 |
| **Reglas de negocio** | RN-03, RN-22 |
| **Requisitos no funcionales** | RNF-10 |

**Criterios de aceptación**

```gherkin
Característica: Cuidar mis compromisos — Que el sistema detecte mis cargos repetidos

  Escenario: Detección de un cargo repetido
    Dado que registré «Gimnasio» por 95.000 en marzo, abril y mayo
    Cuando el sistema revisa mis movimientos
    Entonces me propone convertir ese cargo en suscripción

  Escenario: La propuesta requiere mi confirmación
    Dado que el sistema detectó un cargo repetido
    Cuando no acepto la propuesta
    Entonces no se crea ninguna suscripción

  Escenario: Montos distintos no se proponen
    Dado que registré «Mercado» por montos distintos cada mes
    Cuando el sistema revisa mis movimientos
    Entonces no propone convertirlo en suscripción
```

---

### HU-39 · Dividir un gasto compartido

> **Como** usuario,  
> **quiero** dividir un gasto entre varias personas en una sola operación,  
> **para** registrar de una vez lo que pagué y lo que me deben.

| | |
|---|---|
| **Actividad** | 06 · Cuidar mis compromisos — *Deudas con personas* |
| **Release** | Release 3 · Agente — El sistema trabaja por el usuario |
| **Requisitos de usuario** | RU-11 |
| **Requisitos funcionales** | RF-37 |
| **Reglas de negocio** | RN-11 |
| **Requisitos no funcionales** | RNF-09 |

**Criterios de aceptación**

```gherkin
Característica: Cuidar mis compromisos — Dividir un gasto compartido

  Escenario: División de un gasto entre tres personas
    Cuando registro un gasto de 300.000 y lo divido en partes iguales conmigo, «Camilo» y «Ana»
    Entonces se registra un gasto de 300.000 a mi nombre
    Y se crean dos deudas de 100.000, una por «Camilo» y otra por «Ana»

  Escenario: El abono recibido no cambia el gasto del periodo
    Dado que pagué 300.000 y «Camilo» me debe 100.000
    Cuando «Camilo» me abona 100.000
    Entonces mi gasto del periodo en que pagué sigue siendo 300.000
    Y el saldo pendiente de «Camilo» pasa a cero

  Escenario: La operación es atómica
    Dado que registro un gasto compartido
    Cuando falla la creación de una de las deudas
    Entonces no se guarda el gasto ni ninguna deuda
```

---

### HU-40 · Recordarle la deuda a la otra persona

> **Como** usuario,  
> **quiero** generar un texto con el estado de la deuda y compartirlo por mis canales habituales,  
> **para** cobrar sin tener que redactar el mensaje ni obligar al otro a instalar nada.

| | |
|---|---|
| **Actividad** | 06 · Cuidar mis compromisos — *Deudas con personas* |
| **Release** | Release 3 · Agente — El sistema trabaja por el usuario |
| **Requisitos de usuario** | RU-11 |
| **Requisitos funcionales** | RF-38 |
| **Reglas de negocio** | RN-10 |
| **Requisitos no funcionales** | RNF-14 |

**Criterios de aceptación**

```gherkin
Característica: Cuidar mis compromisos — Recordarle la deuda a la otra persona

  Escenario: Generación del recordatorio
    Dado que «Camilo» me debe 70.000 por «Entradas del concierto» con vencimiento el 30 de mayo
    Cuando pido recordarle la deuda
    Entonces el sistema genera un texto con el concepto, el saldo pendiente y la fecha
    Y lo entrega a los canales de mi dispositivo para compartirlo

  Escenario: La contraparte no necesita cuenta
    Dado que «Camilo» no usa Deshka
    Cuando comparto el recordatorio
    Entonces el mensaje se entrega igual
    Y no se le exige registrarse

  Escenario: El recordatorio está en mi idioma
    Dado que uso la aplicación en inglés
    Cuando genero un recordatorio
    Entonces el texto se redacta en inglés
```

---
