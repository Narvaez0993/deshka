# 02 · Configurar mi dinero

*El usuario declara de dónde sale y a dónde entra su plata.*

**Tareas del story map:** «Registrar mis fuentes» · «Organizar categorías»

| Historia | Título | Release | RF |
|---|---|---|---|
| `HU-07` | Registrar mis cuentas de banco y mi efectivo | Release 1 · MVP | RF-05 |
| `HU-08` | Registrar mi tarjeta de crédito | Release 1 · MVP | RF-06 |
| `HU-09` | Ver un único saldo que ya descuenta lo que debo | Release 1 · MVP | RF-07 |
| `HU-10` | Clasificar mis gastos con el catálogo estándar | Release 1 · MVP | RF-09 |
| `HU-11` | Crear mis propias categorías | Release 2 · Sin fricción | RF-10 |
| `HU-12` | Saber cuándo llegué al límite de fuentes de mi plan | Release 2 · Sin fricción | RF-08 |

---

### HU-07 · Registrar mis cuentas de banco y mi efectivo

> **Como** usuario,  
> **quiero** crear, editar y eliminar mis cuentas bancarias y mi efectivo con su saldo,  
> **para** que la aplicación refleje el dinero que realmente tengo.

| | |
|---|---|
| **Actividad** | 02 · Configurar mi dinero — *Registrar mis fuentes* |
| **Release** | Release 1 · MVP — Registrar y entender lo básico |
| **Requisitos de usuario** | RU-04 |
| **Requisitos funcionales** | RF-05 |
| **Reglas de negocio** | — |
| **Requisitos no funcionales** | RNF-15 |

**Criterios de aceptación**

```gherkin
Característica: Configurar mi dinero — Registrar mis cuentas de banco y mi efectivo

  Escenario: Creación de una cuenta
    Dado que estoy en la sección de mis fuentes de dinero
    Cuando creo una cuenta de tipo bancario con nombre «Nómina» y saldo 800.000
    Entonces la cuenta aparece en mi lista de fuentes con ese saldo
    Y el saldo neto se recalcula incluyéndola

  Escenario: Edición del saldo
    Dado que tengo la cuenta «Nómina» con saldo 800.000
    Cuando corrijo su saldo a 750.000
    Entonces la cuenta queda con saldo 750.000
    Y el saldo neto se recalcula

  Escenario: Eliminación de una fuente con movimientos
    Dado que la cuenta «Nómina» tiene movimientos asociados
    Cuando intento eliminarla
    Entonces el sistema me advierte del efecto sobre esos movimientos antes de confirmar
```

---

### HU-08 · Registrar mi tarjeta de crédito

> **Como** usuario,  
> **quiero** registrar mis tarjetas de crédito con su cupo, su deuda actual, su día de corte y su día de pago,  
> **para** que la aplicación sepa cuánto debo y no solo cuánto tengo.

| | |
|---|---|
| **Actividad** | 02 · Configurar mi dinero — *Registrar mis fuentes* |
| **Release** | Release 1 · MVP — Registrar y entender lo básico |
| **Requisitos de usuario** | RU-04, RU-06 |
| **Requisitos funcionales** | RF-06 |
| **Reglas de negocio** | RN-01 |
| **Requisitos no funcionales** | RNF-15 |

**Criterios de aceptación**

```gherkin
Característica: Configurar mi dinero — Registrar mi tarjeta de crédito

  Escenario: Creación de una tarjeta
    Dado que estoy en la sección de mis fuentes de dinero
    Cuando registro una tarjeta con cupo 5.000.000, deuda actual 1.200.000, corte el día 15 y pago el día 5
    Entonces la tarjeta aparece como una entidad distinta de mis cuentas
    Y el cupo disponible se presenta como 3.800.000

  Escenario: La tarjeta no suma al dinero disponible
    Dado que tengo una cuenta con 800.000 y una tarjeta con deuda 1.200.000
    Cuando consulto mi saldo neto
    Entonces el resultado es -400.000
    Y el cupo de la tarjeta no se cuenta como dinero propio
```

---

### HU-09 · Ver un único saldo que ya descuenta lo que debo

> **Como** usuario,  
> **quiero** ver un saldo neto que reste la deuda de mis tarjetas,  
> **para** no confundir el saldo del banco con mi dinero disponible.

| | |
|---|---|
| **Actividad** | 02 · Configurar mi dinero — *Registrar mis fuentes* |
| **Release** | Release 1 · MVP — Registrar y entender lo básico |
| **Requisitos de usuario** | RU-05 |
| **Requisitos funcionales** | RF-07 |
| **Reglas de negocio** | RN-01 |
| **Requisitos no funcionales** | RNF-02 |

**Criterios de aceptación**

```gherkin
Característica: Configurar mi dinero — Ver un único saldo que ya descuenta lo que debo

  Escenario: Cálculo del saldo neto
    Dado que tengo una cuenta con 900.000, efectivo por 100.000 y una tarjeta con deuda 300.000
    Cuando abro la pantalla de inicio
    Entonces el saldo neto presentado es 700.000

  Escenario: El saldo neto se actualiza con cada movimiento
    Dado que mi saldo neto es 700.000
    Cuando registro un gasto de 50.000 con cargo a mi cuenta bancaria
    Entonces el saldo neto pasa a 650.000

  Escenario: Saldo neto negativo
    Dado que la deuda de mis tarjetas supera la suma de mis cuentas y mi efectivo
    Cuando abro la pantalla de inicio
    Entonces el sistema presenta el saldo neto en negativo
    Y no lo redondea a cero
```

---

### HU-10 · Clasificar mis gastos con el catálogo estándar

> **Como** usuario,  
> **quiero** disponer de un catálogo de categorías de gasto y de ingreso desde el primer día,  
> **para** entender en qué se me va el dinero sin tener que inventar la clasificación.

| | |
|---|---|
| **Actividad** | 02 · Configurar mi dinero — *Organizar categorías* |
| **Release** | Release 1 · MVP — Registrar y entender lo básico |
| **Requisitos de usuario** | RU-07 |
| **Requisitos funcionales** | RF-09 |
| **Reglas de negocio** | RN-20 |
| **Requisitos no funcionales** | RNF-14 |

**Criterios de aceptación**

```gherkin
Característica: Configurar mi dinero — Clasificar mis gastos con el catálogo estándar

  Escenario: Catálogo disponible al crear la cuenta
    Dado que acabo de terminar el onboarding
    Cuando abro el selector de categorías de un gasto
    Entonces encuentro las doce categorías estándar de gasto
    Y encuentro las categorías de ingreso

  Escenario: El catálogo está traducido
    Dado que uso la aplicación en inglés
    Cuando abro el selector de categorías
    Entonces los nombres de las categorías estándar aparecen en inglés
```

---

### HU-11 · Crear mis propias categorías

> **Como** usuario,  
> **quiero** crear categorías con nombre y color propios,  
> **para** clasificar mis gastos como los entiendo yo y no como los entiende el catálogo.

| | |
|---|---|
| **Actividad** | 02 · Configurar mi dinero — *Organizar categorías* |
| **Release** | Release 2 · Sin fricción — Captura asistida y control del gasto |
| **Requisitos de usuario** | RU-07 |
| **Requisitos funcionales** | RF-10 |
| **Reglas de negocio** | RN-19 |
| **Requisitos no funcionales** | RNF-12 |

**Criterios de aceptación**

```gherkin
Característica: Configurar mi dinero — Crear mis propias categorías

  Escenario: Creación de una categoría propia
    Dado que estoy en el plan gratuito y no tengo categorías propias
    Cuando creo la categoría «Mascota» con color morado
    Entonces queda disponible en el selector junto a las estándar

  Escenario: Tope del plan gratuito
    Dado que estoy en el plan gratuito y ya tengo dos categorías propias
    Cuando intento crear una tercera
    Entonces el sistema impide la creación
    Y me informa el límite del plan y la alternativa de mejorarlo

  Escenario: Sin límite en el plan de pago
    Dado que estoy en el plan de pago
    Cuando creo una tercera categoría propia
    Entonces el sistema la crea sin advertencia alguna
```

---

### HU-12 · Saber cuándo llegué al límite de fuentes de mi plan

> **Como** usuario del plan gratuito,  
> **quiero** que el sistema me avise cuando alcanzo el máximo de cuentas o de tarjetas,  
> **para** decidir con información si mejoro mi plan.

| | |
|---|---|
| **Actividad** | 02 · Configurar mi dinero — *Registrar mis fuentes* |
| **Release** | Release 2 · Sin fricción — Captura asistida y control del gasto |
| **Requisitos de usuario** | RU-04, RU-19 |
| **Requisitos funcionales** | RF-08 |
| **Reglas de negocio** | RN-19 |
| **Requisitos no funcionales** | RNF-12 |

**Criterios de aceptación**

```gherkin
Característica: Configurar mi dinero — Saber cuándo llegué al límite de fuentes de mi plan

  Escenario: Límite de cuentas alcanzado
    Dado que estoy en el plan gratuito y ya tengo dos cuentas
    Cuando intento crear una tercera
    Entonces el sistema impide la creación
    Y me informa que el plan gratuito admite dos cuentas
    Y me ofrece la mejora de plan

  Escenario: Límite de tarjetas alcanzado
    Dado que estoy en el plan gratuito y ya tengo una tarjeta de crédito
    Cuando intento registrar una segunda
    Entonces el sistema impide la creación
    Y me informa el límite del plan

  Escenario: El límite no borra lo ya creado al bajar de plan
    Dado que tenía cuatro cuentas en el plan de pago
    Cuando mi plan vuelve a ser gratuito
    Entonces conservo mis cuatro cuentas y su información
    Pero no puedo crear ninguna nueva
```

---
