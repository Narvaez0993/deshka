# Catálogo de historias de usuario

**54 historias** organizadas según el story map: 9 actividades del recorrido del usuario × 3 releases.

Cada historia trae sus criterios de aceptación en **Gherkin** y su trazabilidad hacia los requisitos del Entregable #1 (RU, RF, RN, RNF).

## 01 · [Empezar a usar Deshka](./01-empezar-a-usar-deshka.md)

*El visitante se vuelve usuario y le cuenta al sistema qué quiere lograr.*

| Historia | Título | Tarea | Release | RU | RF |
|---|---|---|---|---|---|
| [`HU-01`](./01-empezar-a-usar-deshka.md#hu-01--crear-mi-cuenta-con-correo-y-contraseña) | Crear mi cuenta con correo y contraseña | Crear mi cuenta | Release 1 · MVP | RU-18, RU-16 | RF-01 |
| [`HU-02`](./01-empezar-a-usar-deshka.md#hu-02--entrar-y-salir-de-mi-cuenta) | Entrar y salir de mi cuenta | Entrar | Release 1 · MVP | RU-18 | RF-02 |
| [`HU-03`](./01-empezar-a-usar-deshka.md#hu-03--onboarding-que-siembra-mis-datos-reales) | Onboarding que siembra mis datos reales | Contar qué quiero lograr | Release 1 · MVP | RU-04, RU-16 | RF-03 |
| [`HU-04`](./01-empezar-a-usar-deshka.md#hu-04--elegir-mi-idioma-mi-tema-y-mi-moneda) | Elegir mi idioma, mi tema y mi moneda | Contar qué quiero lograr | Release 2 · Sin fricción | RU-16 | RF-04 |
| [`HU-05`](./01-empezar-a-usar-deshka.md#hu-05--recuperar-mi-contraseña) | Recuperar mi contraseña | Entrar | Release 3 · Agente | RU-18 | — *sin RF* |
| [`HU-06`](./01-empezar-a-usar-deshka.md#hu-06--entrar-con-google-o-con-apple) | Entrar con Google o con Apple | Entrar | Release 3 · Agente | RU-18 | — *sin RF* |

## 02 · [Configurar mi dinero](./02-configurar-mi-dinero.md)

*El usuario declara de dónde sale y a dónde entra su plata.*

| Historia | Título | Tarea | Release | RU | RF |
|---|---|---|---|---|---|
| [`HU-07`](./02-configurar-mi-dinero.md#hu-07--registrar-mis-cuentas-de-banco-y-mi-efectivo) | Registrar mis cuentas de banco y mi efectivo | Registrar mis fuentes | Release 1 · MVP | RU-04 | RF-05 |
| [`HU-08`](./02-configurar-mi-dinero.md#hu-08--registrar-mi-tarjeta-de-crédito) | Registrar mi tarjeta de crédito | Registrar mis fuentes | Release 1 · MVP | RU-04, RU-06 | RF-06 |
| [`HU-09`](./02-configurar-mi-dinero.md#hu-09--ver-un-único-saldo-que-ya-descuenta-lo-que-debo) | Ver un único saldo que ya descuenta lo que debo | Registrar mis fuentes | Release 1 · MVP | RU-05 | RF-07 |
| [`HU-10`](./02-configurar-mi-dinero.md#hu-10--clasificar-mis-gastos-con-el-catálogo-estándar) | Clasificar mis gastos con el catálogo estándar | Organizar categorías | Release 1 · MVP | RU-07 | RF-09 |
| [`HU-11`](./02-configurar-mi-dinero.md#hu-11--crear-mis-propias-categorías) | Crear mis propias categorías | Organizar categorías | Release 2 · Sin fricción | RU-07 | RF-10 |
| [`HU-12`](./02-configurar-mi-dinero.md#hu-12--saber-cuándo-llegué-al-límite-de-fuentes-de-mi-plan) | Saber cuándo llegué al límite de fuentes de mi plan | Registrar mis fuentes | Release 2 · Sin fricción | RU-04, RU-19 | RF-08 |

## 03 · [Registrar lo que pasa](./03-registrar-lo-que-pasa.md)

*El usuario deja constancia de cada movimiento con el menor esfuerzo posible.*

| Historia | Título | Tarea | Release | RU | RF |
|---|---|---|---|---|---|
| [`HU-13`](./03-registrar-lo-que-pasa.md#hu-13--registrar-un-gasto-a-mano) | Registrar un gasto a mano | Capturar el movimiento | Release 1 · MVP | RU-01 | RF-12 |
| [`HU-14`](./03-registrar-lo-que-pasa.md#hu-14--registrar-el-dinero-que-recibo) | Registrar el dinero que recibo | Capturar el movimiento | Release 1 · MVP | RU-03 | RF-13 |
| [`HU-15`](./03-registrar-lo-que-pasa.md#hu-15--mover-dinero-entre-mis-propias-fuentes) | Mover dinero entre mis propias fuentes | Capturar el movimiento | Release 1 · MVP | RU-05 | RF-14 |
| [`HU-16`](./03-registrar-lo-que-pasa.md#hu-16--usar-y-pagar-la-tarjeta-sin-que-el-gasto-se-cuente-dos-veces) | Usar y pagar la tarjeta sin que el gasto se cuente dos veces | Capturar el movimiento | Release 1 · MVP | RU-06 | RF-21 |
| [`HU-17`](./03-registrar-lo-que-pasa.md#hu-17--registrar-un-gasto-hablando) | Registrar un gasto hablando | Capturar el movimiento | Release 2 · Sin fricción | RU-01 | RF-15 |
| [`HU-18`](./03-registrar-lo-que-pasa.md#hu-18--registrar-un-gasto-escribiendo-en-mis-palabras) | Registrar un gasto escribiendo en mis palabras | Capturar el movimiento | Release 2 · Sin fricción | RU-01 | RF-16 |
| [`HU-19`](./03-registrar-lo-que-pasa.md#hu-19--revisar-y-corregir-lo-que-el-sistema-entendió) | Revisar y corregir lo que el sistema entendió | Confirmar lo que entendió | Release 2 · Sin fricción | RU-02 | RF-18, RF-19 |
| [`HU-20`](./03-registrar-lo-que-pasa.md#hu-20--recibir-una-categoría-sugerida-para-cada-movimiento) | Recibir una categoría sugerida para cada movimiento | Confirmar lo que entendió | Release 2 · Sin fricción | RU-07 | RF-11 |
| [`HU-21`](./03-registrar-lo-que-pasa.md#hu-21--registrar-un-gasto-con-la-foto-del-recibo) | Registrar un gasto con la foto del recibo | Capturar el movimiento | Release 3 · Agente | RU-01 | RF-17 |
| [`HU-22`](./03-registrar-lo-que-pasa.md#hu-22--registrar-aunque-no-tenga-conexión) | Registrar aunque no tenga conexión | Capturar el movimiento | Release 3 · Agente | RU-17 | RF-22 |

## 04 · [Revisar mi día a día](./04-revisar-mi-dia-a-dia.md)

*El usuario mira cómo va y mantiene el historial fiel a la realidad.*

| Historia | Título | Tarea | Release | RU | RF |
|---|---|---|---|---|---|
| [`HU-23`](./04-revisar-mi-dia-a-dia.md#hu-23--consultar-mi-historial-con-filtros) | Consultar mi historial con filtros | Depurar el historial | Release 1 · MVP | RU-15 | RF-20 |
| [`HU-24`](./04-revisar-mi-dia-a-dia.md#hu-24--editar-y-eliminar-movimientos-del-historial) | Editar y eliminar movimientos del historial | Depurar el historial | Release 1 · MVP | RU-15, RU-02 | RF-19 |
| [`HU-25`](./04-revisar-mi-dia-a-dia.md#hu-25--ver-en-el-inicio-cómo-va-mi-mes) | Ver en el inicio cómo va mi mes | Ver cómo voy | Release 1 · MVP | RU-20 | RF-28 |
| [`HU-26`](./04-revisar-mi-dia-a-dia.md#hu-26--comparar-mi-gasto-con-el-mes-pasado) | Comparar mi gasto con el mes pasado | Ver cómo voy | Release 2 · Sin fricción | RU-08 | RF-29 |
| [`HU-27`](./04-revisar-mi-dia-a-dia.md#hu-27--saber-cuánto-ahorré-este-mes) | Saber cuánto ahorré este mes | Ver cómo voy | Release 2 · Sin fricción | RU-03 | RF-30 |

## 05 · [Ponerme límites](./05-ponerme-limites.md)

*El usuario fija un número propio y se mide contra él.*

| Historia | Título | Tarea | Release | RU | RF |
|---|---|---|---|---|---|
| [`HU-28`](./05-ponerme-limites.md#hu-28--ponerme-un-techo-global-de-gasto) | Ponerme un techo global de gasto | Definir el tope | Release 1 · MVP | RU-08 | RF-23 |
| [`HU-29`](./05-ponerme-limites.md#hu-29--saber-cuánto-puedo-gastar-por-día) | Saber cuánto puedo gastar por día | Seguir el consumo | Release 1 · MVP | RU-09 | RF-24 |
| [`HU-30`](./05-ponerme-limites.md#hu-30--ponerme-topes-por-categoría) | Ponerme topes por categoría | Definir el tope | Release 2 · Sin fricción | RU-08 | RF-23 |
| [`HU-31`](./05-ponerme-limites.md#hu-31--que-me-avisen-al-ochenta-por-ciento-y-al-pasarme) | Que me avisen al ochenta por ciento y al pasarme | Seguir el consumo | Release 2 · Sin fricción | RU-08 | RF-26 |
| [`HU-32`](./05-ponerme-limites.md#hu-32--ver-cómo-voy-a-cerrar-el-mes) | Ver cómo voy a cerrar el mes | Seguir el consumo | Release 2 · Sin fricción | RU-08 | RF-25 |
| [`HU-33`](./05-ponerme-limites.md#hu-33--ver-en-qué-comercios-se-me-fue-la-plata) | Ver en qué comercios se me fue la plata | Seguir el consumo | Release 3 · Agente | RU-08 | RF-27 |

## 06 · [Cuidar mis compromisos](./06-cuidar-mis-compromisos.md)

*El usuario no pierde de vista lo que se repite ni lo que debe.*

| Historia | Título | Tarea | Release | RU | RF |
|---|---|---|---|---|---|
| [`HU-34`](./06-cuidar-mis-compromisos.md#hu-34--registrar-mis-suscripciones) | Registrar mis suscripciones | Suscripciones | Release 2 · Sin fricción | RU-10 | RF-31 |
| [`HU-35`](./06-cuidar-mis-compromisos.md#hu-35--confirmar-el-cobro-del-día) | Confirmar el cobro del día | Suscripciones | Release 2 · Sin fricción | RU-10 | RF-32 |
| [`HU-36`](./06-cuidar-mis-compromisos.md#hu-36--que-el-cobro-se-liquide-solo-si-no-respondo) | Que el cobro se liquide solo si no respondo | Suscripciones | Release 2 · Sin fricción | RU-10 | RF-33 |
| [`HU-37`](./06-cuidar-mis-compromisos.md#hu-37--llevar-cuentas-de-lo-que-debo-y-de-lo-que-me-deben) | Llevar cuentas de lo que debo y de lo que me deben | Deudas con personas | Release 2 · Sin fricción | RU-11 | RF-35, RF-36 |
| [`HU-38`](./06-cuidar-mis-compromisos.md#hu-38--que-el-sistema-detecte-mis-cargos-repetidos) | Que el sistema detecte mis cargos repetidos | Suscripciones | Release 3 · Agente | RU-10 | RF-34 |
| [`HU-39`](./06-cuidar-mis-compromisos.md#hu-39--dividir-un-gasto-compartido) | Dividir un gasto compartido | Deudas con personas | Release 3 · Agente | RU-11 | RF-37 |
| [`HU-40`](./06-cuidar-mis-compromisos.md#hu-40--recordarle-la-deuda-a-la-otra-persona) | Recordarle la deuda a la otra persona | Deudas con personas | Release 3 · Agente | RU-11 | RF-38 |

## 07 · [Ahorrar con propósito](./07-ahorrar-con-proposito.md)

*El usuario aparta plata para algo concreto y ve si va a llegar.*

| Historia | Título | Tarea | Release | RU | RF |
|---|---|---|---|---|---|
| [`HU-41`](./07-ahorrar-con-proposito.md#hu-41--crear-una-meta-de-ahorro) | Crear una meta de ahorro | Crear la meta | Release 2 · Sin fricción | RU-12 | RF-39 |
| [`HU-42`](./07-ahorrar-con-proposito.md#hu-42--aportar-y-retirar-dinero-de-mi-meta) | Aportar y retirar dinero de mi meta | Mover plata a la meta | Release 2 · Sin fricción | RU-12 | RF-40 |
| [`HU-43`](./07-ahorrar-con-proposito.md#hu-43--ver-mi-progreso-y-si-voy-a-llegar-a-tiempo) | Ver mi progreso y si voy a llegar a tiempo | Crear la meta | Release 2 · Sin fricción | RU-12 | RF-41 |
| [`HU-44`](./07-ahorrar-con-proposito.md#hu-44--cerrar-y-archivar-una-meta) | Cerrar y archivar una meta | Crear la meta | Release 3 · Agente | RU-12 | RF-42 |

## 08 · [Entender y decidir](./08-entender-y-decidir.md)

*El agente le explica al usuario qué pasó y qué hacer.*

| Historia | Título | Tarea | Release | RU | RF |
|---|---|---|---|---|---|
| [`HU-45`](./08-entender-y-decidir.md#hu-45--recibir-avisos-calculados-sobre-mi-plata) | Recibir avisos calculados sobre mi plata | Recibir avisos | Release 2 · Sin fricción | RU-13, RU-20 | RF-43 |
| [`HU-46`](./08-entender-y-decidir.md#hu-46--preguntarle-al-agente-en-mis-palabras) | Preguntarle al agente en mis palabras | Conversar y revisar | Release 2 · Sin fricción | RU-14 | RF-44 |
| [`HU-47`](./08-entender-y-decidir.md#hu-47--recibir-el-corte-de-mi-mes) | Recibir el corte de mi mes | Recibir avisos | Release 3 · Agente | RU-13 | RF-45 |
| [`HU-48`](./08-entender-y-decidir.md#hu-48--recibir-mi-revisión-semanal) | Recibir mi revisión semanal | Conversar y revisar | Release 3 · Agente | RU-13 | RF-46 |
| [`HU-49`](./08-entender-y-decidir.md#hu-49--aplicar-una-jugada-que-el-agente-me-sugirió) | Aplicar una jugada que el agente me sugirió | Conversar y revisar | Release 3 · Agente | RU-13 | RF-47 |
| [`HU-50`](./08-entender-y-decidir.md#hu-50--volver-a-leer-lo-que-el-agente-ya-me-entregó) | Volver a leer lo que el agente ya me entregó | Recibir avisos | Release 3 · Agente | RU-13 | RF-48 |

## 09 · [Administrar mi plan](./09-administrar-mi-plan.md)

*El usuario sabe qué consume, qué incluye su plan y cómo mejorarlo.*

| Historia | Título | Tarea | Release | RU | RF |
|---|---|---|---|---|---|
| [`HU-51`](./09-administrar-mi-plan.md#hu-51--ver-cuánto-llevo-consumido-de-mi-plan) | Ver cuánto llevo consumido de mi plan | Ver mi consumo | Release 2 · Sin fricción | RU-19 | RF-49 |
| [`HU-52`](./09-administrar-mi-plan.md#hu-52--seguir-registrando-cuando-se-me-acaba-la-cuota) | Seguir registrando cuando se me acaba la cuota | Ver mi consumo | Release 2 · Sin fricción | RU-19, RU-01 | RF-50 |
| [`HU-53`](./09-administrar-mi-plan.md#hu-53--comprar-el-plan-de-pago) | Comprar el plan de pago | Mejorar el plan | Release 3 · Agente | RU-19 | RF-51 |
| [`HU-54`](./09-administrar-mi-plan.md#hu-54--exportar-mis-movimientos) | Exportar mis movimientos | Mejorar el plan | Release 3 · Agente | RU-19, RU-15 | RF-52 |
