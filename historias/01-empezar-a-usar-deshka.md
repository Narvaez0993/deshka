# 01 · Empezar a usar Deshka

*El visitante se vuelve usuario y le cuenta al sistema qué quiere lograr.*

**Tareas del story map:** «Crear mi cuenta» · «Entrar» · «Contar qué quiero lograr»

| Historia | Título | Release | RF |
|---|---|---|---|
| `HU-01` | Crear mi cuenta con correo y contraseña | Release 1 · MVP | RF-01, RF-53 |
| `HU-02` | Entrar y salir de mi cuenta | Release 1 · MVP | RF-02 |
| `HU-03` | Onboarding que siembra mis datos reales | Release 1 · MVP | RF-03 |
| `HU-05` | Recuperar mi contraseña | Release 3 · Agente | RF-54 |
| `HU-06` | Entrar con Google o con Apple | Release 3 · Agente | RF-55 |

---

### HU-01 · Crear mi cuenta con correo y contraseña

> **Como** visitante,  
> **quiero** crear una cuenta con mi correo y una contraseña,  
> **para** que solo yo pueda ver y modificar mi información financiera.

| | |
|---|---|
| **Actividad** | 01 · Empezar a usar Deshka — *Crear mi cuenta* |
| **Release** | Release 1 · MVP — Registrar y entender lo básico |
| **Requisitos de usuario** | RU-18, RU-16 |
| **Requisitos funcionales** | RF-01, RF-53 |
| **Reglas de negocio** | RN-18 |
| **Requisitos no funcionales** | RNF-06, RNF-07 |

**Criterios de aceptación**

```gherkin
Característica: Empezar a usar Deshka — Crear mi cuenta con correo y contraseña

  Escenario: Registro con idioma y moneda tomados de la región
    Dado que soy un visitante sin cuenta
    Y mi dispositivo está configurado en la región «Colombia»
    Cuando envío el formulario de registro con un correo válido y una contraseña de al menos ocho caracteres
    Entonces el sistema crea mi cuenta
    Y toma el idioma «Español» y la moneda «COP» de la región del dispositivo
    Y me deja cambiar la moneda en la configuración inicial

  Escenario: Verificación del correo
    Dado que acabo de crear mi cuenta
    Cuando ingreso el código de verificación que recibí en mi correo
    Entonces mi cuenta queda verificada
    Y puedo iniciar sesión, cosa que el sistema no permite mientras el correo no esté verificado

  Escenario: Correo ya registrado
    Dado que ya existe una cuenta con el correo «ana@correo.com»
    Cuando intento registrarme con ese mismo correo
    Entonces el sistema rechaza el registro
    Y me informa que ese correo ya tiene una cuenta
    Y no crea ninguna cuenta nueva

  Escenario: La contraseña nunca se guarda en texto plano
    Dado que acabo de crear mi cuenta
    Cuando el sistema persiste mis credenciales
    Entonces almacena la contraseña mediante una función de derivación de clave con sal
    Y en ningún momento la conserva en texto plano ni con cifrado reversible
```

---

### HU-02 · Entrar y salir de mi cuenta

> **Como** usuario registrado,  
> **quiero** iniciar sesión con mis credenciales y cerrarla cuando quiera,  
> **para** acceder a mis datos financieros y dejar el dispositivo sin sesión abierta.

| | |
|---|---|
| **Actividad** | 01 · Empezar a usar Deshka — *Entrar* |
| **Release** | Release 1 · MVP — Registrar y entender lo básico |
| **Requisitos de usuario** | RU-18 |
| **Requisitos funcionales** | RF-02 |
| **Reglas de negocio** | — |
| **Requisitos no funcionales** | RNF-07, RNF-08 |

**Criterios de aceptación**

```gherkin
Característica: Empezar a usar Deshka — Entrar y salir de mi cuenta

  Escenario: Inicio de sesión exitoso
    Dado que tengo una cuenta con el correo «ana@correo.com»
    Cuando inicio sesión con ese correo y mi contraseña correcta
    Entonces el sistema emite un token de sesión vigente
    Y me lleva a la pantalla de inicio con mis datos

  Escenario: Credenciales incorrectas
    Dado que tengo una cuenta con el correo «ana@correo.com»
    Cuando inicio sesión con una contraseña equivocada
    Entonces el sistema rechaza el acceso
    Y muestra un mensaje que no revela si el correo existe

  Escenario: Petición sin token vigente
    Dado que mi token de sesión expiró
    Cuando la aplicación solicita cualquier recurso privado
    Entonces el sistema rechaza la petición
    Y la aplicación me devuelve a la pantalla de inicio de sesión

  Escenario: Cierre de sesión
    Dado que tengo la sesión abierta
    Cuando elijo cerrar sesión
    Entonces el sistema invalida el token
    Y el dispositivo deja de conservar mis credenciales
```

---

### HU-03 · Onboarding que siembra mis datos reales

> **Como** usuario nuevo,  
> **quiero** que la aplicación me pregunte mi nombre, mi objetivo financiero y mi primera fuente de dinero,  
> **para** empezar a usarla con información propia y no con datos de ejemplo.

| | |
|---|---|
| **Actividad** | 01 · Empezar a usar Deshka — *Contar qué quiero lograr* |
| **Release** | Release 1 · MVP — Registrar y entender lo básico |
| **Requisitos de usuario** | RU-04, RU-16 |
| **Requisitos funcionales** | RF-03 |
| **Reglas de negocio** | RN-18 |
| **Requisitos no funcionales** | RNF-11 |

**Criterios de aceptación**

```gherkin
Característica: Empezar a usar Deshka — Onboarding que siembra mis datos reales

  Escenario: Onboarding completo persiste datos reales
    Dado que acabo de crear mi cuenta y no he pasado por el onboarding
    Cuando indico mi nombre, elijo el objetivo «Ahorrar para algo» y registro mi primera cuenta con saldo 1.200.000
    Entonces el sistema guarda esos datos como información real de mi cuenta
    Y la pantalla de inicio muestra un saldo de 1.200.000
    Y no se crea ningún movimiento ni fuente de ejemplo

  Escenario: El objetivo declarado orienta la pantalla de inicio
    Dado que declaré el objetivo «Controlar en qué se me va la plata»
    Cuando abro la pantalla de inicio
    Entonces la información principal corresponde a ese objetivo

  Escenario: Onboarding incompleto no deja la cuenta a medias
    Dado que abandono el onboarding antes de registrar mi primera fuente
    Cuando vuelvo a abrir la aplicación
    Entonces el sistema retoma el onboarding en el paso pendiente
```

---

### HU-05 · Recuperar mi contraseña

> **Como** usuario que olvidó su contraseña,  
> **quiero** restablecerla desde mi correo,  
> **para** recuperar el acceso a mi información sin perder mis datos.

| | |
|---|---|
| **Actividad** | 01 · Empezar a usar Deshka — *Entrar* |
| **Release** | Release 3 · Agente — El sistema trabaja por el usuario |
| **Requisitos de usuario** | RU-18 |
| **Requisitos funcionales** | RF-54 |
| **Reglas de negocio** | — |
| **Requisitos no funcionales** | RNF-06, RNF-07 |

**Criterios de aceptación**

```gherkin
Característica: Empezar a usar Deshka — Recuperar mi contraseña

  Escenario: Solicitud de restablecimiento
    Dado que olvidé mi contraseña
    Cuando solicito restablecerla indicando mi correo
    Entonces el sistema envía un enlace de un solo uso con vigencia limitada
    Y responde igual exista o no una cuenta con ese correo

  Escenario: Restablecimiento efectivo
    Dado que abrí un enlace de restablecimiento vigente
    Cuando defino una contraseña nueva
    Entonces el sistema la almacena derivada con sal
    Y invalida el enlace
    Y cierra las sesiones abiertas de mi cuenta

  Escenario: Enlace vencido
    Dado que el enlace de restablecimiento expiró
    Cuando intento usarlo
    Entonces el sistema lo rechaza
    Y me ofrece solicitar uno nuevo
```

---

### HU-06 · Entrar con Google o con Apple

> **Como** visitante,  
> **quiero** crear mi cuenta y entrar con mi identidad de Google o de Apple,  
> **para** empezar a usar la aplicación sin inventar otra contraseña.

| | |
|---|---|
| **Actividad** | 01 · Empezar a usar Deshka — *Entrar* |
| **Release** | Release 3 · Agente — El sistema trabaja por el usuario |
| **Requisitos de usuario** | RU-18 |
| **Requisitos funcionales** | RF-55 |
| **Reglas de negocio** | — |
| **Requisitos no funcionales** | RNF-07 |

**Criterios de aceptación**

```gherkin
Característica: Empezar a usar Deshka — Entrar con Google o con Apple

  Escenario: Alta con proveedor externo
    Dado que no tengo cuenta en Deshka
    Cuando entro con mi identidad de Google
    Entonces el sistema crea mi cuenta con el correo verificado del proveedor
    Y me lleva al onboarding

  Escenario: Vinculación con una cuenta existente
    Dado que ya tengo una cuenta creada con el correo «ana@correo.com»
    Cuando entro con una identidad externa que reporta ese mismo correo verificado
    Entonces el sistema vincula el proveedor a mi cuenta existente
    Y no crea una cuenta duplicada
```

---
