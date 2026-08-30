# -*- coding: utf-8 -*-
"""Actividades 04 y 05 del story map."""

from model import Historia

HU = [
    Historia(
        id="HU-23",
        titulo="Consultar mi historial con filtros",
        actividad="04", tarea="Depurar el historial", release="R1",
        rol="usuario",
        quiero="listar mis movimientos y filtrarlos por periodo, tipo, categoría y fuente",
        para="encontrar lo que busco sin recorrer toda la lista",
        ru=["RU-15"], rf=["RF-20"], rn=[], rnf=["RNF-02"],
        escenarios=[
            ("Listado del periodo en curso", [
                "Dado que tengo movimientos registrados en varios meses",
                "Cuando abro el historial",
                "Entonces veo los movimientos del mes en curso ordenados del más reciente al más antiguo",
            ]),
            ("Filtro combinado", [
                "Dado que estoy en el historial",
                "Cuando filtro por tipo «gasto», categoría «Transporte» y fuente «Visa»",
                "Entonces solo veo los movimientos que cumplen las tres condiciones",
            ]),
            ("Los movimientos especiales quedan señalados", [
                "Dado que tengo una transferencia y un gasto originado en una suscripción",
                "Cuando los veo en el historial",
                "Entonces la transferencia aparece marcada como transferencia",
                "Y el gasto de la suscripción aparece marcado como recurrente",
            ]),
            ("Rendimiento del listado", [
                "Dado que mi cuenta tiene mil movimientos registrados",
                "Cuando abro el historial",
                "Entonces la lista se presenta en menos de dos segundos",
            ]),
        ],
    ),
    Historia(
        id="HU-24",
        titulo="Editar y eliminar movimientos del historial",
        actividad="04", tarea="Depurar el historial", release="R1",
        rol="usuario",
        quiero="corregir o borrar cualquier movimiento que registré",
        para="mantener el historial fiel a lo que realmente ocurrió",
        ru=["RU-15", "RU-02"], rf=["RF-19"], rn=["RN-27"], rnf=["RNF-09"],
        escenarios=[
            ("Edición del monto de un gasto", [
                "Dado que registré un gasto de 50.000 con cargo a «Nómina», que quedó en 750.000",
                "Cuando cambio el monto del gasto a 30.000",
                "Entonces «Nómina» queda en 770.000",
                "Y el gasto del mes se recalcula",
            ]),
            ("Eliminación de un consumo con tarjeta", [
                "Dado que registré un consumo de 150.000 con la tarjeta, cuya deuda quedó en 1.150.000",
                "Cuando elimino ese movimiento",
                "Entonces la deuda de la tarjeta vuelve a 1.000.000",
                "Y el gasto del mes disminuye en 150.000",
            ]),
            ("Eliminación de un aporte a una meta", [
                "Dado que aporté 100.000 a la meta «Viaje»",
                "Cuando elimino ese aporte",
                "Entonces lo ahorrado de la meta disminuye en 100.000",
                "Y el saldo de la cuenta de origen aumenta en 100.000",
            ]),
            ("Confirmación antes de borrar", [
                "Cuando pido eliminar un movimiento",
                "Entonces el sistema me pide confirmar",
                "Y solo entonces revierte sus efectos",
            ]),
        ],
    ),
    Historia(
        id="HU-25",
        titulo="Ver en el inicio cómo va mi mes",
        actividad="04", tarea="Ver cómo voy", release="R1",
        rol="usuario",
        quiero="que la pantalla de inicio me muestre el ritmo de mi mes según el objetivo que declaré",
        para="entender mi situación de un vistazo y sin interpretar gráficas",
        ru=["RU-20"], rf=["RF-28"], rn=["RN-03", "RN-04"], rnf=["RNF-02", "RNF-12"],
        escenarios=[
            ("La vista se adapta al objetivo declarado", [
                "Dado que declaré el objetivo «Ahorrar para algo»",
                "Cuando abro la pantalla de inicio",
                "Entonces la información principal corresponde al avance de mis metas",
            ]),
            ("Nunca una figura sin datos", [
                "Dado que no tengo ningún tope de gasto definido",
                "Cuando abro la pantalla de inicio",
                "Entonces no se presenta ninguna barra ni cifra de consumo de tope",
                "Y en su lugar se me ofrece definir uno",
            ]),
            ("Ninguna cifra inventada", [
                "Dado que no definí ningún tope",
                "Cuando abro la pantalla de inicio",
                "Entonces el sistema no presenta ningún gasto diario permitido derivado de mis ingresos",
            ]),
        ],
    ),
    Historia(
        id="HU-26",
        titulo="Comparar mi gasto con el mes pasado",
        actividad="04", tarea="Ver cómo voy", release="R2",
        rol="usuario",
        quiero="comparar lo que llevo gastado con el mismo tramo del mes anterior",
        para="saber si voy mejor o peor que la última vez",
        ru=["RU-08"], rf=["RF-29"], rn=["RN-09"], rnf=["RNF-02"],
        escenarios=[
            ("Comparación sobre el mismo tramo de días", [
                "Dado que hoy es 10 de mayo y llevo 400.000 gastados",
                "Y entre el 1 y el 10 de abril gasté 500.000",
                "Cuando abro la pantalla de inicio",
                "Entonces el sistema informa que voy 100.000 por debajo del mes anterior",
                "Y no compara contra el total de abril",
            ]),
            ("Sin historial comparable", [
                "Dado que es mi primer mes usando la aplicación",
                "Cuando abro la pantalla de inicio",
                "Entonces la comparación con el mes anterior se omite",
                "Y no se muestra una variación de cero por ciento",
            ]),
        ],
    ),
    Historia(
        id="HU-27",
        titulo="Saber cuánto ahorré este mes",
        actividad="04", tarea="Ver cómo voy", release="R2",
        rol="usuario",
        quiero="ver la diferencia entre lo que recibí y lo que gasté en el mes",
        para="medir mi ahorro y no solamente mis salidas de dinero",
        ru=["RU-03"], rf=["RF-30"], rn=["RN-03"], rnf=["RNF-02"],
        escenarios=[
            ("Cálculo de la tasa de ahorro", [
                "Dado que este mes registré ingresos por 3.000.000 y gastos por 2.100.000",
                "Cuando consulto mi tasa de ahorro",
                "Entonces el sistema informa 900.000 ahorrados, equivalentes al treinta por ciento de mis ingresos",
            ]),
            ("Las transferencias no alteran el cálculo", [
                "Dado que transferí 500.000 entre dos cuentas mías",
                "Cuando consulto mi tasa de ahorro",
                "Entonces el resultado no cambia por esa transferencia",
            ]),
            ("Sin ingresos registrados", [
                "Dado que no registré ningún ingreso este mes",
                "Cuando consulto mi tasa de ahorro",
                "Entonces el sistema no presenta un porcentaje",
                "Y me invita a registrar mis ingresos",
            ]),
        ],
    ),

    # ---------------------------------------------------------------- 05
    Historia(
        id="HU-28",
        titulo="Ponerme un techo global de gasto",
        actividad="05", tarea="Definir el tope", release="R1",
        rol="usuario",
        quiero="fijar un tope general de gasto para el mes y ver cuánto llevo consumido",
        para="medirme contra un número que yo elegí",
        ru=["RU-08"], rf=["RF-23"], rn=["RN-04", "RN-05", "RN-06"], rnf=["RNF-15"],
        escenarios=[
            ("Definición del techo global", [
                "Dado que no tengo ningún tope definido",
                "Cuando fijo un techo global de 2.500.000 para el mes",
                "Entonces la pantalla de inicio muestra el consumo del techo",
            ]),
            ("Todo gasto cuenta contra el techo", [
                "Dado que tengo un techo global de 2.500.000 y llevo 1.000.000 gastados",
                "Cuando registro un gasto de 50.000 en una categoría sin tope propio",
                "Entonces el consumo del techo global pasa a 1.050.000",
            ]),
            ("El tope sigue vigente el mes siguiente", [
                "Dado que definí un techo global en mayo y no lo he modificado",
                "Cuando comienza junio",
                "Entonces el mismo techo rige para junio",
                "Y el consumo se reinicia en cero",
            ]),
            ("Modificar el tope aplica al mes en curso", [
                "Dado que llevo 1.000.000 consumidos de un techo de 2.500.000",
                "Cuando cambio el techo a 2.000.000",
                "Entonces el consumo del mes en curso pasa a medirse contra 2.000.000",
            ]),
        ],
    ),
    Historia(
        id="HU-29",
        titulo="Saber cuánto puedo gastar por día",
        actividad="05", tarea="Seguir el consumo", release="R1",
        rol="usuario",
        quiero="ver cuánto puedo gastar diariamente en lo que resta del mes",
        para="no pasarme del tope que definí",
        ru=["RU-09"], rf=["RF-24"], rn=["RN-04", "RN-07"], rnf=["RNF-02"],
        escenarios=[
            ("Cálculo del techo diario", [
                "Dado que tengo un techo de 3.000.000, llevo 1.500.000 gastados y quedan diez días de mes contando hoy",
                "Cuando abro la pantalla de inicio",
                "Entonces el sistema informa 150.000 disponibles por día",
            ]),
            ("Sin tope definido no hay cifra diaria", [
                "Dado que no definí ningún tope",
                "Cuando abro la pantalla de inicio",
                "Entonces el sistema no presenta ninguna cifra de gasto diario",
                "Y me ofrece definir un tope",
            ]),
            ("Tope superado", [
                "Dado que gasté 3.200.000 de un techo de 3.000.000",
                "Cuando abro la pantalla de inicio",
                "Entonces el sistema informa un exceso de 200.000",
                "Y no presenta un disponible en cero ni una cifra diaria",
            ]),
        ],
    ),
    Historia(
        id="HU-30",
        titulo="Ponerme topes por categoría",
        actividad="05", tarea="Definir el tope", release="R2",
        rol="usuario",
        quiero="fijar un tope para categorías concretas y ver el consumo de cada una",
        para="controlar los rubros que se me desbordan",
        ru=["RU-08"], rf=["RF-23"], rn=["RN-05", "RN-19"], rnf=["RNF-12"],
        escenarios=[
            ("Definición de un tope por categoría", [
                "Dado que tengo un techo global de 2.500.000",
                "Cuando fijo un tope de 400.000 para «Alimentación»",
                "Entonces veo el consumo de «Alimentación» contra sus 400.000",
            ]),
            ("Los topes por categoría no son acumulables", [
                "Dado que tengo un techo global de 2.500.000 y topes de 400.000 y 300.000 en dos categorías",
                "Cuando registro un gasto de 100.000 en «Alimentación»",
                "Entonces el consumo de «Alimentación» aumenta en 100.000",
                "Y el consumo del techo global también aumenta en 100.000",
            ]),
            ("Tope del plan gratuito", [
                "Dado que estoy en el plan gratuito y ya tengo dos topes por categoría",
                "Cuando intento crear un tercero",
                "Entonces el sistema impide la creación",
                "Y me informa el límite del plan",
            ]),
        ],
    ),
    Historia(
        id="HU-31",
        titulo="Que me avisen al ochenta por ciento y al pasarme",
        actividad="05", tarea="Seguir el consumo", release="R2",
        rol="usuario",
        quiero="recibir un aviso cuando un tope llega al ochenta por ciento y cuando lo supero",
        para="reaccionar antes de que sea tarde",
        ru=["RU-08"], rf=["RF-26"], rn=["RN-07"], rnf=["RNF-12"],
        escenarios=[
            ("Aviso al ochenta por ciento", [
                "Dado que tengo un tope de 400.000 en «Alimentación» y llevo 300.000",
                "Cuando registro un gasto de 25.000 en esa categoría",
                "Entonces el sistema me avisa que consumí el ochenta por ciento del tope",
            ]),
            ("Aviso al superar el tope", [
                "Dado que tengo un tope de 400.000 en «Alimentación» y llevo 390.000",
                "Cuando registro un gasto de 30.000 en esa categoría",
                "Entonces el sistema me avisa que superé el tope",
                "Y me informa un exceso de 20.000",
            ]),
            ("El aviso no se repite por cada gasto", [
                "Dado que ya recibí el aviso del ochenta por ciento de «Alimentación» este mes",
                "Cuando registro otro gasto en esa categoría sin superar el tope",
                "Entonces el sistema no vuelve a emitir el mismo aviso",
            ]),
        ],
    ),
    Historia(
        id="HU-32",
        titulo="Ver cómo voy a cerrar el mes",
        actividad="05", tarea="Seguir el consumo", release="R2",
        rol="usuario",
        quiero="ver una proyección de mi cierre del mes según el ritmo que llevo",
        para="corregir a tiempo si voy camino de pasarme",
        ru=["RU-08"], rf=["RF-25"], rn=["RN-08"], rnf=["RNF-02"],
        escenarios=[
            ("Proyección contrastada con el tope", [
                "Dado que tengo un techo de 3.000.000, llevo 1.200.000 gastados y transcurrieron diez de treinta días",
                "Cuando abro la pantalla de inicio",
                "Entonces el sistema proyecta un cierre de 3.600.000",
                "Y advierte que superaría el techo en 600.000",
            ]),
            ("Sin proyección al comenzar el mes", [
                "Dado que hoy es el segundo día del mes",
                "Cuando abro la pantalla de inicio",
                "Entonces el sistema no emite proyección de cierre",
                "Y explica que aún no hay base suficiente",
            ]),
        ],
    ),
    Historia(
        id="HU-33",
        titulo="Ver en qué comercios se me fue la plata",
        actividad="05", tarea="Seguir el consumo", release="R3",
        rol="usuario",
        quiero="ver, en cada categoría con tope, los tres comercios donde más gasté",
        para="saber qué concretamente está consumiendo mi tope",
        ru=["RU-08"], rf=["RF-27"], rn=[], rnf=["RNF-02"],
        escenarios=[
            ("Los tres comercios de mayor gasto", [
                "Dado que tengo un tope en «Alimentación» con gastos en varios comercios",
                "Cuando abro el detalle de esa categoría",
                "Entonces veo los tres comercios de mayor gasto del periodo con su monto",
            ]),
            ("Agrupación insensible a mayúsculas y espacios", [
                "Dado que registré gastos con las descripciones «exito», «Éxito» y « EXITO »",
                "Cuando abro el detalle de la categoría",
                "Entonces los tres aparecen agrupados como un solo comercio",
            ]),
            ("Categoría sin gastos", [
                "Dado que una categoría con tope no tiene gastos en el periodo",
                "Cuando abro su detalle",
                "Entonces el sistema no presenta la lista de comercios",
            ]),
        ],
    ),
]
