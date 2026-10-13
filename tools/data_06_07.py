# -*- coding: utf-8 -*-
"""Actividades 06 y 07 del story map."""

from model import Historia

HU = [
    Historia(
        id="HU-34",
        titulo="Registrar mis suscripciones",
        actividad="06", tarea="Suscripciones", release="R2",
        rol="usuario",
        quiero="crear, editar, pausar y eliminar mis cobros recurrentes",
        para="que ningún cobro me tome por sorpresa",
        ru=["RU-10"], rf=["RF-31"], rn=["RN-16", "RN-17"], rnf=["RNF-15"],
        escenarios=[
            ("Creación de una suscripción", [
                "Dado que estoy en la sección de suscripciones",
                "Cuando registro «Streaming» por 26.900 mensuales con cobro el día 8",
                "Entonces la suscripción aparece en mi lista con su próximo cobro",
                "Y ningún saldo de mis fuentes cambia",
            ]),
            ("La suscripción no genera cobros anteriores a su registro", [
                "Dado que hoy es 20 de mayo",
                "Cuando registro una suscripción con cobro el día 8",
                "Entonces el primer cobro previsto es el 8 de junio",
                "Y no se crea ningún cobro del 8 de mayo",
            ]),
            ("Pausar una suscripción", [
                "Dado que tengo la suscripción «Streaming» activa",
                "Cuando la pauso",
                "Entonces deja de generar cobros pendientes",
                "Y conserva su historial",
            ]),
        ],
    ),
    Historia(
        id="HU-35",
        titulo="Confirmar el cobro del día",
        actividad="06", tarea="Suscripciones", release="R2",
        rol="usuario",
        quiero="que el sistema me pregunte el día del cobro si se realizó, si lo omito o si pauso la suscripción",
        para="que solo se registre el dinero que de verdad salió",
        ru=["RU-10"], rf=["RF-32"], rn=["RN-16"], rnf=["RNF-10"],
        escenarios=[
            ("Apertura del cobro pendiente", [
                "Dado que tengo la suscripción «Streaming» con cobro el día 8",
                "Cuando llega el día 8",
                "Entonces el sistema abre un cobro pendiente",
                "Y me ofrece confirmarlo, omitirlo o pausar la suscripción",
            ]),
            ("Confirmación del cobro", [
                "Dado que tengo un cobro pendiente de 26.900",
                "Cuando lo confirmo",
                "Entonces se registra un gasto de 26.900 en la fuente asociada",
                "Y el cobro pendiente se cierra",
            ]),
            ("Omisión del cobro", [
                "Dado que tengo un cobro pendiente de 26.900",
                "Cuando lo omito",
                "Entonces no se registra ningún gasto",
                "Y la suscripción conserva su próximo cobro para el periodo siguiente",
            ]),
            ("Ejecución idempotente", [
                "Dado que el proceso automático ya abrió el cobro del día 8",
                "Cuando el proceso vuelve a ejecutarse sobre ese mismo día",
                "Entonces no se crea un segundo cobro pendiente",
            ]),
        ],
    ),
    Historia(
        id="HU-36",
        titulo="Que el cobro se liquide solo si no respondo",
        actividad="06", tarea="Suscripciones", release="R2",
        rol="usuario",
        quiero="que el cobro pendiente se registre automáticamente si no respondo en tres horas, y poder revertirlo",
        para="que mi historial no dependa de que yo esté pendiente del teléfono",
        ru=["RU-10"], rf=["RF-33"], rn=["RN-16"], rnf=["RNF-10"],
        escenarios=[
            ("Liquidación automática", [
                "Dado que tengo un cobro pendiente de 26.900 abierto hace tres horas",
                "Cuando no he respondido",
                "Entonces el sistema registra el gasto",
                "Y lo marca como registrado automáticamente",
            ]),
            ("Reversión de un cobro automático", [
                "Dado que el sistema liquidó automáticamente un cobro de 26.900",
                "Cuando lo revierto",
                "Entonces el gasto se elimina",
                "Y el saldo de la fuente vuelve a su valor anterior",
            ]),
            ("Respuesta dentro de la ventana", [
                "Dado que tengo un cobro pendiente abierto hace una hora",
                "Cuando lo omito",
                "Entonces el sistema no lo liquida automáticamente después",
            ]),
        ],
    ),
    Historia(
        id="HU-37",
        titulo="Llevar cuentas de lo que debo y de lo que me deben",
        actividad="06", tarea="Deudas con personas", release="R2",
        rol="usuario",
        quiero="registrar deudas con personas y sus abonos parciales",
        para="no perder la cuenta de préstamos y gastos compartidos",
        ru=["RU-11"], rf=["RF-35", "RF-36"], rn=["RN-10", "RN-12"], rnf=["RNF-09"],
        escenarios=[
            ("Registro de una deuda a mi favor", [
                "Cuando registro que «Camilo» me debe 120.000 por «Entradas del concierto» con vencimiento el 30 de mayo",
                "Entonces la deuda aparece con saldo pendiente 120.000",
                "Y ningún saldo de mis fuentes cambia",
            ]),
            ("Abono parcial", [
                "Dado que «Camilo» me debe 120.000",
                "Cuando registro un abono de 50.000",
                "Entonces el saldo pendiente pasa a 70.000",
                "Y la deuda sigue en estado pendiente",
            ]),
            ("Abono que salda la deuda", [
                "Dado que «Camilo» me debe 70.000",
                "Cuando registro un abono de 70.000",
                "Entonces el saldo pendiente pasa a cero",
                "Y la deuda queda en estado saldada",
            ]),
            ("Abono superior al saldo pendiente", [
                "Dado que «Camilo» me debe 70.000",
                "Cuando intento registrar un abono de 100.000",
                "Entonces el sistema rechaza el abono y me lo informa",
                "Y no lo ajusta automáticamente a 70.000",
            ]),
            ("Deshacer el último abono", [
                "Dado que registré por error un abono de 50.000",
                "Cuando deshago el último abono",
                "Entonces el saldo pendiente vuelve a su valor anterior",
            ]),
        ],
    ),
    Historia(
        id="HU-38",
        titulo="Que el sistema detecte mis cargos repetidos",
        actividad="06", tarea="Suscripciones", release="R3",
        rol="usuario",
        quiero="que el sistema identifique gastos que se repiten y me proponga convertirlos en suscripción",
        para="no tener que acordarme de registrarlos yo",
        ru=["RU-10"], rf=["RF-34"], rn=["RN-03", "RN-22"], rnf=["RNF-10"],
        escenarios=[
            ("Detección de un cargo repetido", [
                "Dado que registré «Gimnasio» por 95.000 en marzo, abril y mayo",
                "Cuando el sistema revisa mis movimientos",
                "Entonces me propone convertir ese cargo en suscripción",
            ]),
            ("La propuesta requiere mi confirmación", [
                "Dado que el sistema detectó un cargo repetido",
                "Cuando no acepto la propuesta",
                "Entonces no se crea ninguna suscripción",
            ]),
            ("Montos distintos no se proponen", [
                "Dado que registré «Mercado» por montos distintos cada mes",
                "Cuando el sistema revisa mis movimientos",
                "Entonces no propone convertirlo en suscripción",
            ]),
        ],
    ),
    Historia(
        id="HU-39",
        titulo="Dividir un gasto compartido",
        actividad="06", tarea="Deudas con personas", release="R3",
        rol="usuario",
        quiero="dividir un gasto entre varias personas en una sola operación",
        para="registrar de una vez lo que pagué y lo que me deben",
        ru=["RU-11"], rf=["RF-37"], rn=["RN-11"], rnf=["RNF-09"],
        escenarios=[
            ("División de un gasto entre tres personas", [
                "Cuando registro un gasto de 300.000 y lo divido en partes iguales conmigo, «Camilo» y «Ana»",
                "Entonces se registra un gasto de 300.000 a mi nombre",
                "Y se crean dos deudas de 100.000, una por «Camilo» y otra por «Ana»",
            ]),
            ("El abono recibido no cambia el gasto del periodo", [
                "Dado que pagué 300.000 y «Camilo» me debe 100.000",
                "Cuando «Camilo» me abona 100.000",
                "Entonces mi gasto del periodo en que pagué sigue siendo 300.000",
                "Y el saldo pendiente de «Camilo» pasa a cero",
            ]),
            ("La operación es atómica", [
                "Dado que registro un gasto compartido",
                "Cuando falla la creación de una de las deudas",
                "Entonces no se guarda el gasto ni ninguna deuda",
            ]),
        ],
    ),
    Historia(
        id="HU-40",
        titulo="Recordarle la deuda a la otra persona",
        actividad="06", tarea="Deudas con personas", release="R3",
        rol="usuario",
        quiero="generar un texto con el estado de la deuda y compartirlo por mis canales habituales",
        para="cobrar sin tener que redactar el mensaje ni obligar al otro a instalar nada",
        ru=["RU-11"], rf=["RF-38"], rn=["RN-10"], rnf=["RNF-14"],
        escenarios=[
            ("Generación del recordatorio", [
                "Dado que «Camilo» me debe 70.000 por «Entradas del concierto» con vencimiento el 30 de mayo",
                "Cuando pido recordarle la deuda",
                "Entonces el sistema genera un texto con el concepto, el saldo pendiente y la fecha",
                "Y lo entrega a los canales de mi dispositivo para compartirlo",
            ]),
            ("La contraparte no necesita cuenta", [
                "Dado que «Camilo» no usa Deshka",
                "Cuando comparto el recordatorio",
                "Entonces el mensaje se entrega igual",
                "Y no se le exige registrarse",
            ]),
            ("El recordatorio está en mi idioma", [
                "Dado que uso la aplicación en inglés",
                "Cuando genero un recordatorio",
                "Entonces el texto se redacta en inglés",
            ]),
        ],
    ),

    # ---------------------------------------------------------------- 07
    Historia(
        id="HU-41",
        titulo="Crear una meta de ahorro",
        actividad="07", tarea="Crear la meta", release="R2",
        rol="usuario",
        quiero="crear una meta con nombre, monto objetivo y fecha opcional",
        para="que ahorrar deje de ser una intención vaga",
        ru=["RU-12"], rf=["RF-39"], rn=["RN-19"], rnf=["RNF-15"],
        escenarios=[
            ("Creación de una meta", [
                "Cuando creo la meta «Viaje» por 4.000.000 con fecha objetivo el 15 de diciembre",
                "Entonces la meta aparece activa con 0 ahorrados",
            ]),
            ("Meta sin fecha objetivo", [
                "Cuando creo la meta «Fondo de emergencia» por 6.000.000 sin fecha",
                "Entonces el sistema la acepta",
                "Y no exige una fecha para operarla",
            ]),
            ("Tope del plan gratuito", [
                "Dado que estoy en el plan gratuito y ya tengo una meta activa",
                "Cuando intento crear otra",
                "Entonces el sistema impide la creación",
                "Y me informa el límite del plan",
            ]),
        ],
    ),
    Historia(
        id="HU-42",
        titulo="Aportar y retirar dinero de mi meta",
        actividad="07", tarea="Mover plata a la meta", release="R2",
        rol="usuario",
        quiero="apartar dinero para la meta y poder devolverlo cuando lo necesite",
        para="que el ahorro sea plata real y no una cifra declarada",
        ru=["RU-12"], rf=["RF-40"], rn=["RN-13", "RN-14"], rnf=["RNF-09"],
        escenarios=[
            ("Aporte a la meta", [
                "Dado que «Nómina» tiene 1.000.000 y la meta «Viaje» tiene 0 ahorrados",
                "Cuando aporto 300.000 desde «Nómina»",
                "Entonces «Nómina» queda en 700.000 y la meta en 300.000",
                "Y el gasto del mes no cambia",
            ]),
            ("Retiro desde la meta", [
                "Dado que la meta «Viaje» tiene 300.000 apartados",
                "Cuando retiro 100.000 hacia «Nómina»",
                "Entonces la meta queda en 200.000 y «Nómina» aumenta en 100.000",
                "Y el ingreso del mes no cambia",
            ]),
            ("Retiro superior a lo apartado", [
                "Dado que la meta «Viaje» tiene 200.000 apartados",
                "Cuando intento retirar 250.000",
                "Entonces el sistema rechaza el retiro y me lo informa",
            ]),
        ],
    ),
    Historia(
        id="HU-43",
        titulo="Ver mi progreso y si voy a llegar a tiempo",
        actividad="07", tarea="Seguir y cerrar la meta", release="R2",
        rol="usuario",
        quiero="ver cuánto llevo ahorrado y una estimación de cuándo cumpliré la meta",
        para="saber si mi ritmo alcanza o si tengo que aportar más",
        ru=["RU-12"], rf=["RF-41"], rn=["RN-14"], rnf=["RNF-02", "RNF-23"],
        escenarios=[
            ("Lo ahorrado se deriva de los movimientos", [
                "Dado que aporté 300.000 y retiré 100.000 de la meta «Viaje»",
                "Cuando consulto la meta",
                "Entonces lo ahorrado es 200.000",
                "Y esa cifra proviene de sus movimientos y no de un valor almacenado aparte",
            ]),
            ("Aporte mensual necesario con fecha objetivo", [
                "Dado que la meta «Viaje» es de 4.000.000, lleva 1.000.000 y vence en seis meses",
                "Cuando consulto su proyección",
                "Entonces el sistema informa que necesito aportar 500.000 mensuales",
            ]),
            ("Fecha estimada sin fecha objetivo", [
                "Dado que la meta «Fondo de emergencia» no tiene fecha y vengo aportando 200.000 al mes",
                "Cuando consulto su proyección",
                "Entonces el sistema estima la fecha de cumplimiento según ese ritmo",
            ]),
            ("Sin historial de aportes", [
                "Dado que la meta no tiene aportes todavía",
                "Cuando consulto su proyección",
                "Entonces el sistema no presenta una fecha estimada",
            ]),
        ],
    ),
    Historia(
        id="HU-44",
        titulo="Cerrar y archivar una meta",
        actividad="07", tarea="Seguir y cerrar la meta", release="R3",
        rol="usuario",
        quiero="archivar o eliminar una meta cuando ya no la necesito",
        para="mantener mi lista limpia sin perder lo que ya logré",
        ru=["RU-12"], rf=["RF-42"], rn=["RN-15"], rnf=[],
        escenarios=[
            ("Archivar una meta cumplida", [
                "Dado que la meta «Viaje» no conserva dinero apartado",
                "Cuando la archivo",
                "Entonces sale de mis metas activas",
                "Y conservo su historial",
            ]),
            ("Meta con dinero apartado", [
                "Dado que la meta «Viaje» conserva 200.000 apartados",
                "Cuando intento archivarla o eliminarla",
                "Entonces el sistema lo impide",
                "Y me pide retirar primero el dinero",
            ]),
            ("Archivar libera el cupo del plan gratuito", [
                "Dado que estoy en el plan gratuito con una meta activa sin dinero apartado",
                "Cuando la archivo",
                "Entonces puedo crear una meta nueva",
            ]),
        ],
    ),
]
