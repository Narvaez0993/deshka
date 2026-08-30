# Diagrama de clases de diseño

Estructura del sistema Deshka: **17 clases** con sus atributos, sus operaciones y las relaciones
entre ellas. Corresponde al **numeral 4 del Entregable #1**.

Está escrito contra el dominio real del backend: los nombres de clases y atributos son los que
existen en el código.

## Enlaces

| | |
|---|---|
| 🖼️ **Imagen (PNG)** | [`assets/diagrama-de-clases.png`](../assets/diagrama-de-clases.png) |
| 🖼️ **Imagen (SVG, vectorial)** | [`assets/diagrama-de-clases.svg`](../assets/diagrama-de-clases.svg) |
| ✏️ **Abrir en PlantUML (editable)** | https://www.plantuml.com/plantuml/uml/5Sp13S8m3030FrF008sHUBMlJi0EnhQQYCIfR8TAdHvutUzM3xGOhLvkHQaEbckEs7q1C3pILYAFrt0nwXgYaQWtUA9zKCxxF3-0nVCReM5Hu4uEN70pR3YnJ5JHnTF-_rTH_la5 |
| 📄 **Código fuente** | [`docs/diagrama-de-clases.puml`](./diagrama-de-clases.puml) |

Las imágenes del repositorio son la versión canónica: son las que van al documento. El enlace de
PlantUML abre el **modelo** en la herramienta, donde puede consultarse y editarse; su render usa
Graphviz en vez de Smetana, así que ordena las mismas clases de otra manera.

![Diagrama de clases de Deshka](../assets/diagrama-de-clases.png)

## Cómo leer el diagrama

**`User` es dueño de todo.** Cada entidad del sistema pertenece a un usuario y jamás se consulta sin
él: es una relación de composición, porque nada sobrevive al borrado de la cuenta.

**`FundingSource` es la abstracción central.** Una cuenta de banco, una tarjeta de crédito y una meta
de ahorro son todas *lugares donde hay plata*, y comparten un único contrato: reciben un delta y lo
aplican. Una cuenta lo suma al saldo; una tarjeta lo **resta** a la deuda. De esa sola diferencia
sale toda la contabilidad de tarjeta de crédito, sin casos especiales.

**`Movement` es el libro mayor.** Un único tipo de registro para gasto, ingreso y transferencia. El
monto es siempre positivo y el signo lo determina `type`, lo que hace imposible el estado
contradictorio de un gasto negativo.

**Lo derivado no se guarda.** `Debt.remaining()`, `Goal.saved()` y `Budget.spent()` son operaciones,
no atributos, precisamente porque se calculan al leer. Un derivado almacenado es un campo que se
desactualiza.

### Nota sobre `FundingSource`

Es una abstracción de **diseño**. En la implementación, cuentas, tarjetas y metas viven en
colecciones separadas y el movimiento las referencia por un par `(tipo, id)` que se resuelve al
aplicar los deltas — el efecto es el mismo polimorfismo, resuelto por composición en vez de herencia.

## Versión detallada (anexo)

El modelo completo, con objetos de valor, clases derivadas, la jerarquía de errores de dominio y los
puertos entre módulos de la arquitectura hexagonal: **51 clases, 19 enumeraciones y 9 interfaces en
13 paquetes**.

| | |
|---|---|
| 🖼️ **Imagen** | [`assets/diagrama-de-clases-detallado.png`](../assets/diagrama-de-clases-detallado.png) · [SVG](../assets/diagrama-de-clases-detallado.svg) |
| ✏️ **Abrir el modelo en PlantUML** | https://www.plantuml.com/plantuml/uml/5SvB4e8m44NHkQlG1K12WbHmn0hSmoFTVCf0gAIZLQvU7Dqpl4CM92bRkDpMtOT2V5r4ZlnGAk5JpwiiPIoPau-xy2wrZvjw8ht1NzttLX7dvGNbsLXdR7TloS4PQD8TzHqid6wfyLF3PhJjf2Zwh6Z5dB2X8gvyGEPyIX02ADR7_sRWdSx-00 |
| 📄 **Código fuente** | [`docs/diagrama-de-clases-detallado.puml`](./diagrama-de-clases-detallado.puml) |

## Regenerar

Requiere Java y `plantuml.jar` ([plantuml.com/download](https://plantuml.com/download)).

```bash
java -DPLANTUML_LIMIT_SIZE=32768 -jar plantuml.jar -Playout=smetana -tpng -Sdpi=150 -o assets docs/diagrama-de-clases.puml
```
