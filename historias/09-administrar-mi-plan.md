# 09 · Administrar mi plan

*El usuario sabe qué consume, qué incluye su plan y cómo mejorarlo.*

**Tareas del story map:** «Ver mi consumo» · «Mejorar el plan»

| Historia | Título | Release | RF |
|---|---|---|---|
| `HU-51` | Ver cuánto llevo consumido de mi plan | Release 2 · Sin fricción | RF-49 |
| `HU-52` | Seguir registrando cuando se me acaba la cuota | Release 2 · Sin fricción | RF-50 |
| `HU-53` | Comprar el plan de pago | Release 3 · Agente | RF-51 |
| `HU-54` | Exportar mis movimientos | Release 3 · Agente | RF-52 |

---

### HU-51 · Ver cuánto llevo consumido de mi plan

> **Como** usuario,  
> **quiero** ver mis dos contadores mensuales de uso de inteligencia artificial,  
> **para** saber en qué punto estoy antes de quedarme sin cuota.

| | |
|---|---|
| **Actividad** | 09 · Administrar mi plan — *Ver mi consumo* |
| **Release** | Release 2 · Sin fricción — Captura asistida y control del gasto |
| **Requisitos de usuario** | RU-19 |
| **Requisitos funcionales** | RF-49 |
| **Reglas de negocio** | RN-19, RN-20, RN-21 |
| **Requisitos no funcionales** | RNF-22 |

**Criterios de aceptación**

```gherkin
Característica: Administrar mi plan — Ver cuánto llevo consumido de mi plan

  Escenario: Dos contadores independientes
    Dado que estoy en el plan gratuito
    Cuando consulto mi consumo
    Entonces veo los registros asistidos usados sobre sesenta
    Y los mensajes con el agente usados sobre diez

  Escenario: Reinicio al cambiar el periodo
    Dado que agoté mis sesenta registros asistidos en mayo
    Cuando comienza junio
    Entonces ambos contadores vuelven a cero

  Escenario: Lo que no consume cuota
    Dado que registro movimientos a mano y recibo entregas automáticas del agente
    Cuando consulto mi consumo
    Entonces ninguno de los dos contadores se incrementó por esas operaciones
```

---

### HU-52 · Seguir registrando cuando se me acaba la cuota

> **Como** usuario del plan gratuito,  
> **quiero** que al agotar mis registros asistidos la aplicación me deje el formulario manual prellenado,  
> **para** no quedarme sin poder registrar.

| | |
|---|---|
| **Actividad** | 09 · Administrar mi plan — *Ver mi consumo* |
| **Release** | Release 2 · Sin fricción — Captura asistida y control del gasto |
| **Requisitos de usuario** | RU-19, RU-01 |
| **Requisitos funcionales** | RF-50 |
| **Reglas de negocio** | RN-19, RN-20 |
| **Requisitos no funcionales** | RNF-12 |

**Criterios de aceptación**

```gherkin
Característica: Administrar mi plan — Seguir registrando cuando se me acaba la cuota

  Escenario: Degradación al formulario manual
    Dado que agoté mis sesenta registros asistidos del mes
    Cuando intento registrar por voz
    Entonces el sistema me ofrece el formulario manual prellenado con lo que pueda derivar sin consumir cuota
    Y me informa que la captura asistida se reanuda el mes siguiente

  Escenario: Margen de cortesía en los mensajes del agente
    Dado que agoté mis diez mensajes con el agente
    Cuando le escribo
    Entonces el sistema me concede el margen de cortesía definido antes de bloquear el envío

  Escenario: Bloqueo informado, no silencioso
    Dado que agoté la cuota y el margen de cortesía
    Cuando intento escribirle al agente
    Entonces el sistema me explica el límite alcanzado y me ofrece mejorar el plan
```

---

### HU-53 · Comprar el plan de pago

> **Como** usuario del plan gratuito,  
> **quiero** contratar la suscripción desde la tienda de aplicaciones,  
> **para** levantar los topes de capacidad de mi plan.

| | |
|---|---|
| **Actividad** | 09 · Administrar mi plan — *Mejorar el plan* |
| **Release** | Release 3 · Agente — El sistema trabaja por el usuario |
| **Requisitos de usuario** | RU-19 |
| **Requisitos funcionales** | RF-51 |
| **Reglas de negocio** | RN-19 |
| **Requisitos no funcionales** | RNF-07 |

**Criterios de aceptación**

```gherkin
Característica: Administrar mi plan — Comprar el plan de pago

  Escenario: Compra confirmada
    Dado que estoy en el plan gratuito
    Cuando completo la compra en la tienda de aplicaciones
    Y el sistema recibe la confirmación del proveedor
    Entonces mi plan pasa a ser de pago
    Y los límites de capacidad se levantan de inmediato

  Escenario: Compra cancelada
    Cuando cancelo la compra en la tienda
    Entonces mi plan sigue siendo gratuito
    Y no se altera ningún límite

  Escenario: Sin confirmación del proveedor no hay beneficios
    Dado que la tienda aún no confirma el pago
    Cuando abro la aplicación
    Entonces conservo el plan gratuito hasta recibir la confirmación
```

---

### HU-54 · Exportar mis movimientos

> **Como** usuario,  
> **quiero** descargar mis movimientos en un archivo,  
> **para** conservar mi información por fuera de la aplicación.

| | |
|---|---|
| **Actividad** | 09 · Administrar mi plan — *Mejorar el plan* |
| **Release** | Release 3 · Agente — El sistema trabaja por el usuario |
| **Requisitos de usuario** | RU-19, RU-15 |
| **Requisitos funcionales** | RF-52 |
| **Reglas de negocio** | RN-19 |
| **Requisitos no funcionales** | RNF-15, RNF-19 |

**Criterios de aceptación**

```gherkin
Característica: Administrar mi plan — Exportar mis movimientos

  Escenario: Exportación en el plan gratuito
    Dado que estoy en el plan gratuito y no he exportado este mes
    Cuando solicito la exportación
    Entonces el sistema genera el archivo con mis movimientos

  Escenario: Segunda exportación del mes en el plan gratuito
    Dado que ya exporté una vez este mes en el plan gratuito
    Cuando solicito exportar de nuevo
    Entonces el sistema lo impide
    Y me informa el límite del plan

  Escenario: Exportación sin límite en el plan de pago
    Dado que estoy en el plan de pago
    Cuando solicito la exportación por segunda vez en el mes
    Entonces el sistema genera el archivo sin advertencia

  Escenario: Los montos conservan su formato
    Dado que mi moneda es «COP»
    Cuando abro el archivo exportado
    Entonces los montos aparecen en la unidad menor de la moneda con su formato regional
```

---
