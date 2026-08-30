# -*- coding: utf-8 -*-
"""Actividades 08 y 09 del story map."""

from model import Historia

HU = [
    Historia(
        id="HU-45",
        titulo="Recibir avisos calculados sobre mi plata",
        actividad="08", tarea="Recibir avisos", release="R2",
        rol="usuario",
        quiero="recibir avisos derivados de mis propios datos, cada uno con algo que pueda hacer",
        para="enterarme de lo importante sin tener que ir a buscarlo",
        ru=["RU-13", "RU-20"], rf=["RF-43"], rn=["RN-03", "RN-22"], rnf=["RNF-12", "RNF-21"],
        escenarios=[
            ("Aviso generado por una regla sobre mis datos", [
                "Dado que tengo un cobro de «Streaming» previsto para dentro de dos días",
                "Cuando abro el feed",
                "Entonces veo un aviso de ese cobro próximo",
                "Y el aviso ofrece una acción que me lleva a la suscripción",
            ]),
            ("Ningún aviso sobre datos no registrados", [
                "Dado que no registré ningún movimiento este mes",
                "Cuando abro el feed",
                "Entonces no aparece ningún aviso que afirme conductas mías",
            ]),
            ("Todo aviso tiene acción", [
                "Dado que el feed tiene avisos",
                "Cuando reviso cada uno",
                "Entonces todos ejecutan una acción o navegan a la pantalla correspondiente",
            ]),
        ],
    ),
    Historia(
        id="HU-46",
        titulo="Preguntarle al agente en mis palabras",
        actividad="08", tarea="Conversar y revisar", release="R2",
        rol="usuario",
        quiero="conversar con la aplicación y preguntarle por mis gastos, topes, metas, deudas y suscripciones",
        para="resolver dudas puntuales sin navegar entre pantallas",
        ru=["RU-14"], rf=["RF-44"], rn=["RN-03", "RN-19", "RN-23"], rnf=["RNF-03", "RNF-05"],
        escenarios=[
            ("Pregunta respondida con datos propios", [
                "Dado que este mes gasté 320.000 en «Transporte»",
                "Cuando le pregunto «¿cuánto llevo en transporte?»",
                "Entonces el agente responde 320.000",
                "Y esa cifra proviene del cálculo del sistema y no de la redacción del modelo",
            ]),
            ("Respuesta en mi idioma", [
                "Dado que uso la aplicación en inglés",
                "Cuando le escribo al agente",
                "Entonces responde en inglés",
            ]),
            ("Pregunta fuera de lo registrado", [
                "Cuando le pregunto algo que mis datos no permiten responder",
                "Entonces el agente dice que no cuenta con esa información",
                "Y no inventa una cifra",
            ]),
            ("Consumo de la cuota de mensajes", [
                "Dado que estoy en el plan gratuito y llevo nueve mensajes en el mes",
                "Cuando envío otro mensaje al agente",
                "Entonces el contador pasa a diez",
            ]),
            ("Falla del proveedor de inteligencia artificial", [
                "Dado que el proveedor de inteligencia artificial no responde",
                "Cuando le escribo al agente",
                "Entonces el sistema me informa la indisponibilidad",
                "Y no presenta cifras inventadas ni una pantalla de error sin explicación",
            ]),
        ],
    ),
    Historia(
        id="HU-47",
        titulo="Recibir el corte de mi mes",
        actividad="08", tarea="Recibir avisos", release="R3",
        rol="usuario",
        quiero="recibir al comenzar el mes un resumen narrado del mes anterior",
        para="entender qué pasó con mi plata sin interpretar gráficas",
        ru=["RU-13"], rf=["RF-45"], rn=["RN-21", "RN-23", "RN-24"], rnf=["RNF-05", "RNF-10", "RNF-21"],
        escenarios=[
            ("Composición del cierre mensual", [
                "Dado que el mes anterior registré más de tres movimientos",
                "Cuando comienza el mes nuevo",
                "Entonces el sistema compone un resumen del mes anterior en secuencia de pantallas",
                "Y omite las pantallas que no tengan datos",
            ]),
            ("Mes sin actividad suficiente", [
                "Dado que el mes anterior registré dos movimientos",
                "Cuando comienza el mes nuevo",
                "Entonces no se genera cierre mensual",
            ]),
            ("El cierre no consume mi cuota", [
                "Dado que estoy en el plan gratuito",
                "Cuando recibo el cierre del mes",
                "Entonces mis contadores de uso no se incrementan",
            ]),
            ("Falla del proveedor durante la composición", [
                "Dado que el proveedor de inteligencia artificial falla al redactar el cierre",
                "Cuando el sistema entrega el resumen",
                "Entonces lo presenta con plantillas fijas sin cifras",
                "Y no omite la entrega ni muestra un error",
            ]),
            ("Ejecución idempotente", [
                "Dado que el proceso ya generó el cierre de abril",
                "Cuando vuelve a ejecutarse sobre ese periodo",
                "Entonces no se produce una segunda entrega",
            ]),
        ],
    ),
    Historia(
        id="HU-48",
        titulo="Recibir mi revisión semanal",
        actividad="08", tarea="Conversar y revisar", release="R3",
        rol="usuario",
        quiero="recibir cada semana un diagnóstico, hasta tres acciones sugeridas y el resultado de las de la semana pasada",
        para="corregir el rumbo con algo concreto y saber si lo anterior sirvió",
        ru=["RU-13"], rf=["RF-46"], rn=["RN-21", "RN-22", "RN-23"], rnf=["RNF-10", "RNF-21"],
        escenarios=[
            ("Entrega semanal", [
                "Dado que cerró una semana con movimientos registrados",
                "Cuando el sistema genera la revisión",
                "Entonces recibo el diagnóstico de esa semana",
                "Y hasta tres acciones sugeridas",
            ]),
            ("Rendición de cuentas de la semana anterior", [
                "Dado que la semana pasada acepté la acción «tope de 200.000 en Restaurantes»",
                "Cuando recibo la revisión de esta semana",
                "Entonces incluye el resultado de esa acción",
            ]),
            ("Semana sin movimientos", [
                "Dado que no registré movimientos en la semana que cerró",
                "Cuando el sistema genera la revisión",
                "Entonces no presenta un diagnóstico con cifras",
            ]),
        ],
    ),
    Historia(
        id="HU-49",
        titulo="Aplicar una jugada que el agente me sugirió",
        actividad="08", tarea="Conversar y revisar", release="R3",
        rol="usuario",
        quiero="aceptar una acción sugerida y que se convierta en un tope o en un aporte real",
        para="que el consejo se materialice sin que yo lo tenga que configurar",
        ru=["RU-13"], rf=["RF-47"], rn=["RN-22"], rnf=["RNF-12"],
        escenarios=[
            ("Acción que crea un tope", [
                "Dado que el agente sugiere un tope de 200.000 en «Restaurantes»",
                "Cuando la aplico",
                "Entonces el tope queda creado con ese monto",
                "Y la acción aparece como aplicada",
            ]),
            ("Acción que crea un aporte", [
                "Dado que el agente sugiere aportar 150.000 a la meta «Viaje»",
                "Cuando la aplico",
                "Entonces se registra el aporte como transferencia real desde la cuenta que elegí",
            ]),
            ("Nada se aplica sin mi confirmación", [
                "Dado que el agente sugiere una acción",
                "Cuando no la acepto",
                "Entonces no se modifica ningún dato financiero",
            ]),
            ("Aplicación fallida", [
                "Dado que el agente sugiere un aporte de 150.000",
                "Y la cuenta de origen no tiene saldo suficiente",
                "Cuando intento aplicarla",
                "Entonces el sistema muestra el estado de falla y su motivo",
                "Y no registra el aporte",
            ]),
        ],
    ),
    Historia(
        id="HU-50",
        titulo="Volver a leer lo que el agente ya me entregó",
        actividad="08", tarea="Recibir avisos", release="R3",
        rol="usuario",
        quiero="que los cierres del mes y las revisiones queden archivados aunque los descarte del feed",
        para="poder releerlos cuando quiera",
        ru=["RU-13"], rf=["RF-48"], rn=[], rnf=[],
        escenarios=[
            ("Descartar no elimina", [
                "Dado que tengo el cierre de abril en el feed",
                "Cuando lo descarto",
                "Entonces desaparece del feed",
                "Y sigue disponible en el archivo de entregas",
            ]),
            ("Consulta del archivo", [
                "Dado que tengo varias entregas archivadas",
                "Cuando abro el archivo",
                "Entonces las veo ordenadas por periodo",
                "Y puedo abrir cualquiera completa",
            ]),
        ],
    ),

    # ---------------------------------------------------------------- 09
    Historia(
        id="HU-51",
        titulo="Ver cuánto llevo consumido de mi plan",
        actividad="09", tarea="Ver mi consumo", release="R2",
        rol="usuario",
        quiero="ver mis dos contadores mensuales de uso de inteligencia artificial",
        para="saber en qué punto estoy antes de quedarme sin cuota",
        ru=["RU-19"], rf=["RF-49"], rn=["RN-19", "RN-20", "RN-21"], rnf=["RNF-22"],
        escenarios=[
            ("Dos contadores independientes", [
                "Dado que estoy en el plan gratuito",
                "Cuando consulto mi consumo",
                "Entonces veo los registros asistidos usados sobre sesenta",
                "Y los mensajes con el agente usados sobre diez",
            ]),
            ("Reinicio al cambiar el periodo", [
                "Dado que agoté mis sesenta registros asistidos en mayo",
                "Cuando comienza junio",
                "Entonces ambos contadores vuelven a cero",
            ]),
            ("Lo que no consume cuota", [
                "Dado que registro movimientos a mano y recibo entregas automáticas del agente",
                "Cuando consulto mi consumo",
                "Entonces ninguno de los dos contadores se incrementó por esas operaciones",
            ]),
        ],
    ),
    Historia(
        id="HU-52",
        titulo="Seguir registrando cuando se me acaba la cuota",
        actividad="09", tarea="Ver mi consumo", release="R2",
        rol="usuario del plan gratuito",
        quiero="que al agotar mis registros asistidos la aplicación me deje el formulario manual prellenado",
        para="no quedarme sin poder registrar",
        ru=["RU-19", "RU-01"], rf=["RF-50"], rn=["RN-19", "RN-20"], rnf=["RNF-12"],
        escenarios=[
            ("Degradación al formulario manual", [
                "Dado que agoté mis sesenta registros asistidos del mes",
                "Cuando intento registrar por voz",
                "Entonces el sistema me ofrece el formulario manual prellenado con lo que pueda derivar sin consumir cuota",
                "Y me informa que la captura asistida se reanuda el mes siguiente",
            ]),
            ("Margen de cortesía en los mensajes del agente", [
                "Dado que agoté mis diez mensajes con el agente",
                "Cuando le escribo",
                "Entonces el sistema me concede el margen de cortesía definido antes de bloquear el envío",
            ]),
            ("Bloqueo informado, no silencioso", [
                "Dado que agoté la cuota y el margen de cortesía",
                "Cuando intento escribirle al agente",
                "Entonces el sistema me explica el límite alcanzado y me ofrece mejorar el plan",
            ]),
        ],
    ),
    Historia(
        id="HU-53",
        titulo="Comprar el plan de pago",
        actividad="09", tarea="Mejorar el plan", release="R3",
        rol="usuario del plan gratuito",
        quiero="contratar la suscripción desde la tienda de aplicaciones",
        para="levantar los topes de capacidad de mi plan",
        ru=["RU-19"], rf=["RF-51"], rn=["RN-19"], rnf=["RNF-07"],
        escenarios=[
            ("Compra confirmada", [
                "Dado que estoy en el plan gratuito",
                "Cuando completo la compra en la tienda de aplicaciones",
                "Y el sistema recibe la confirmación del proveedor",
                "Entonces mi plan pasa a ser de pago",
                "Y los límites de capacidad se levantan de inmediato",
            ]),
            ("Compra cancelada", [
                "Cuando cancelo la compra en la tienda",
                "Entonces mi plan sigue siendo gratuito",
                "Y no se altera ningún límite",
            ]),
            ("Sin confirmación del proveedor no hay beneficios", [
                "Dado que la tienda aún no confirma el pago",
                "Cuando abro la aplicación",
                "Entonces conservo el plan gratuito hasta recibir la confirmación",
            ]),
        ],
    ),
    Historia(
        id="HU-54",
        titulo="Exportar mis movimientos",
        actividad="09", tarea="Mejorar el plan", release="R3",
        rol="usuario",
        quiero="descargar mis movimientos en un archivo",
        para="conservar mi información por fuera de la aplicación",
        ru=["RU-19", "RU-15"], rf=["RF-52"], rn=["RN-19"], rnf=["RNF-15", "RNF-19"],
        escenarios=[
            ("Exportación en el plan gratuito", [
                "Dado que estoy en el plan gratuito y no he exportado este mes",
                "Cuando solicito la exportación",
                "Entonces el sistema genera el archivo con mis movimientos",
            ]),
            ("Segunda exportación del mes en el plan gratuito", [
                "Dado que ya exporté una vez este mes en el plan gratuito",
                "Cuando solicito exportar de nuevo",
                "Entonces el sistema lo impide",
                "Y me informa el límite del plan",
            ]),
            ("Exportación sin límite en el plan de pago", [
                "Dado que estoy en el plan de pago",
                "Cuando solicito la exportación por segunda vez en el mes",
                "Entonces el sistema genera el archivo sin advertencia",
            ]),
            ("Los montos conservan su formato", [
                "Dado que mi moneda es «COP»",
                "Cuando abro el archivo exportado",
                "Entonces los montos aparecen en la unidad menor de la moneda con su formato regional",
            ]),
        ],
    ),
]
