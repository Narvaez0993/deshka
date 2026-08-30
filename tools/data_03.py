# -*- coding: utf-8 -*-
"""Actividad 03 del story map: registrar lo que pasa."""

from model import Historia

HU = [
    Historia(
        id="HU-13",
        titulo="Registrar un gasto a mano",
        actividad="03", tarea="Capturar el movimiento", release="R1",
        rol="usuario",
        quiero="registrar un gasto indicando monto, descripción, fuente, categoría y fecha",
        para="dejar constancia exacta de lo que salió, sin depender de ninguna interpretación automática",
        ru=["RU-01"], rf=["RF-12"], rn=["RN-20"], rnf=["RNF-15"],
        escenarios=[
            ("Registro de un gasto con cargo a una cuenta", [
                "Dado que tengo la cuenta «Nómina» con saldo 800.000",
                "Cuando registro un gasto de 45.000 con descripción «Mercado», categoría «Alimentación», fuente «Nómina» y la fecha de hoy",
                "Entonces el movimiento queda guardado",
                "Y el saldo de «Nómina» pasa a 755.000",
                "Y el gasto del mes aumenta en 45.000",
            ]),
            ("El registro manual no consume cuota", [
                "Dado que estoy en el plan gratuito y agoté mis registros asistidos del mes",
                "Cuando registro un gasto a mano",
                "Entonces el sistema lo guarda con normalidad",
                "Y ningún contador de uso de inteligencia artificial se incrementa",
            ]),
            ("Monto inválido", [
                "Dado que estoy diligenciando un gasto",
                "Cuando indico un monto igual a cero o negativo",
                "Entonces el sistema rechaza el guardado",
                "Y señala el campo del monto",
            ]),
        ],
    ),
    Historia(
        id="HU-14",
        titulo="Registrar el dinero que recibo",
        actividad="03", tarea="Capturar el movimiento", release="R1",
        rol="usuario",
        quiero="registrar un ingreso con su monto, su fuente de destino y su fecha",
        para="saber cuánto ahorro y no solamente cuánto gasto",
        ru=["RU-03"], rf=["RF-13"], rn=[], rnf=["RNF-15"],
        escenarios=[
            ("Registro de un ingreso", [
                "Dado que tengo la cuenta «Nómina» con saldo 200.000",
                "Cuando registro un ingreso de 3.000.000 con descripción «Salario» y destino «Nómina»",
                "Entonces el saldo de «Nómina» pasa a 3.200.000",
                "Y el ingreso del mes aumenta en 3.000.000",
            ]),
            ("La categoría de ingreso es opcional", [
                "Dado que estoy registrando un ingreso",
                "Cuando lo guardo sin elegir categoría",
                "Entonces el sistema lo acepta",
                "Y lo presenta en el historial como ingreso sin categoría",
            ]),
            ("El ingreso no cuenta como gasto", [
                "Dado que tengo un tope global de gasto definido",
                "Cuando registro un ingreso",
                "Entonces el consumo del tope no cambia",
            ]),
        ],
    ),
    Historia(
        id="HU-15",
        titulo="Mover dinero entre mis propias fuentes",
        actividad="03", tarea="Capturar el movimiento", release="R1",
        rol="usuario",
        quiero="registrar traslados entre dos fuentes mías",
        para="que mis saldos queden fieles sin que el traslado se cuente como gasto",
        ru=["RU-05"], rf=["RF-14"], rn=["RN-13"], rnf=["RNF-09"],
        escenarios=[
            ("Transferencia entre dos cuentas", [
                "Dado que tengo «Nómina» con 1.000.000 y «Ahorros» con 500.000",
                "Cuando transfiero 200.000 de «Nómina» a «Ahorros»",
                "Entonces «Nómina» queda en 800.000 y «Ahorros» en 700.000",
                "Y ni el gasto ni el ingreso del mes cambian",
            ]),
            ("La transferencia es atómica", [
                "Dado que una transferencia está en curso",
                "Cuando falla la actualización de la fuente de destino",
                "Entonces el sistema no descuenta la fuente de origen",
                "Y ningún saldo queda modificado a medias",
            ]),
            ("Origen y destino no pueden ser la misma fuente", [
                "Dado que estoy registrando una transferencia",
                "Cuando elijo la misma fuente como origen y como destino",
                "Entonces el sistema rechaza la operación",
            ]),
        ],
    ),
    Historia(
        id="HU-16",
        titulo="Usar y pagar la tarjeta sin que el gasto se cuente dos veces",
        actividad="03", tarea="Capturar el movimiento", release="R1",
        rol="usuario con tarjeta de crédito",
        quiero="que el consumo con tarjeta sea gasto y que el pago de la tarjeta no vuelva a serlo",
        para="que mi presupuesto no se descuadre",
        ru=["RU-06"], rf=["RF-21"], rn=["RN-01", "RN-02"], rnf=["RNF-09"],
        escenarios=[
            ("El consumo con tarjeta es gasto y aumenta la deuda", [
                "Dado que mi tarjeta tiene una deuda de 1.000.000",
                "Cuando registro un gasto de 150.000 con cargo a la tarjeta",
                "Entonces el gasto del mes aumenta en 150.000",
                "Y la deuda de la tarjeta pasa a 1.150.000",
                "Y ningún saldo de mis cuentas cambia",
            ]),
            ("El pago de la tarjeta es transferencia y no gasto", [
                "Dado que mi tarjeta tiene una deuda de 1.150.000 y «Nómina» tiene 900.000",
                "Cuando registro un pago de 500.000 a la tarjeta desde «Nómina»",
                "Entonces la deuda de la tarjeta pasa a 650.000",
                "Y «Nómina» queda en 400.000",
                "Y el gasto del mes no cambia",
            ]),
            ("Compra a cuotas", [
                "Dado que mi tarjeta tiene una deuda de 0",
                "Cuando registro una compra de 1.200.000 a doce cuotas",
                "Entonces la deuda de la tarjeta aumenta en 1.200.000 en el momento de la compra",
                "Y el gasto del mes aumenta en 1.200.000",
                "Y cada cuota que pague después se registra como transferencia y no como gasto nuevo",
            ]),
            ("La operación es atómica", [
                "Dado que registro un consumo con tarjeta",
                "Cuando falla la actualización de la deuda",
                "Entonces el movimiento no queda guardado",
                "Y ni el gasto del mes ni la deuda quedan modificados",
            ]),
        ],
    ),
    Historia(
        id="HU-17",
        titulo="Registrar un gasto hablando",
        actividad="03", tarea="Capturar el movimiento", release="R2",
        rol="usuario",
        quiero="dictar lo que gasté y que el sistema arme el movimiento",
        para="no abandonar el registro por el esfuerzo que exige la digitación",
        ru=["RU-01"], rf=["RF-15"], rn=["RN-19", "RN-23"], rnf=["RNF-01", "RNF-11"],
        escenarios=[
            ("Dictado interpretado", [
                "Dado que tengo la cuenta «Nómina» y la tarjeta «Visa»",
                "Cuando dicto «gasté treinta mil en el almuerzo con la Visa»",
                "Entonces el sistema propone un gasto de 30.000 con descripción «almuerzo», categoría «Alimentación», fuente «Visa» y la fecha de hoy",
                "Y me presenta la pantalla de confirmación en menos de cinco segundos",
            ]),
            ("El dictado consume un registro asistido", [
                "Dado que llevo diez registros asistidos consumidos en el mes",
                "Cuando guardo un movimiento capturado por voz",
                "Entonces el contador de registros asistidos pasa a once",
            ]),
            ("Dictado incomprensible", [
                "Dado que dicto una frase sin monto reconocible",
                "Cuando el sistema termina de interpretarla",
                "Entonces me presenta el formulario manual con lo que sí pudo derivar",
                "Y no guarda ningún movimiento por su cuenta",
            ]),
        ],
    ),
    Historia(
        id="HU-18",
        titulo="Registrar un gasto escribiendo en mis palabras",
        actividad="03", tarea="Capturar el movimiento", release="R2",
        rol="usuario",
        quiero="escribir una frase en lenguaje natural y que el sistema derive los campos del movimiento",
        para="registrar sin diligenciar un formulario campo por campo",
        ru=["RU-01"], rf=["RF-16"], rn=["RN-19", "RN-23"], rnf=["RNF-11"],
        escenarios=[
            ("Frase interpretada", [
                "Cuando escribo «12.000 de taxi ayer»",
                "Entonces el sistema propone un gasto de 12.000 con descripción «taxi», categoría «Transporte» y la fecha de ayer",
            ]),
            ("Frase que describe un ingreso", [
                "Cuando escribo «me pagaron 3 millones del salario»",
                "Entonces el sistema propone un ingreso de 3.000.000 y no un gasto",
            ]),
            ("Fuente no mencionada", [
                "Dado que tengo más de una fuente de dinero",
                "Cuando escribo una frase que no menciona con qué pagué",
                "Entonces el sistema deja la fuente sin preseleccionar",
                "Y me pide elegirla antes de guardar",
            ]),
        ],
    ),
    Historia(
        id="HU-19",
        titulo="Revisar y corregir lo que el sistema entendió",
        actividad="03", tarea="Confirmar lo que entendió", release="R2",
        rol="usuario",
        quiero="ver los campos interpretados y poder editarlos antes de guardar",
        para="confiar en la información aunque la interpretación automática se equivoque",
        ru=["RU-02"], rf=["RF-18", "RF-19"], rn=["RN-22"], rnf=["RNF-11", "RNF-12"],
        escenarios=[
            ("Confirmación antes de guardar", [
                "Dado que capturé un movimiento por voz, por texto o por foto",
                "Cuando el sistema termina de interpretarlo",
                "Entonces me muestra monto, descripción, categoría, fuente y fecha en campos editables",
                "Y nada queda guardado hasta que confirmo",
            ]),
            ("Corrección de un campo interpretado", [
                "Dado que el sistema propuso la categoría «Alimentación»",
                "Cuando la cambio a «Entretenimiento» y confirmo",
                "Entonces el movimiento se guarda con la categoría que yo elegí",
            ]),
            ("Corrección después de guardar", [
                "Dado que guardé un movimiento con un monto equivocado",
                "Cuando lo edito e indico el monto correcto",
                "Entonces el sistema revierte el efecto anterior sobre los saldos y aplica el nuevo",
            ]),
            ("Descartar la interpretación", [
                "Dado que el sistema entendió algo que no corresponde",
                "Cuando descarto la propuesta",
                "Entonces no se guarda ningún movimiento",
            ]),
        ],
    ),
    Historia(
        id="HU-20",
        titulo="Recibir una categoría sugerida para cada movimiento",
        actividad="03", tarea="Confirmar lo que entendió", release="R2",
        rol="usuario",
        quiero="que el sistema proponga la categoría de lo que registro",
        para="no tener que clasificar cada movimiento a mano",
        ru=["RU-07"], rf=["RF-11"], rn=["RN-20"], rnf=["RNF-11"],
        escenarios=[
            ("Sugerencia sobre una descripción conocida", [
                "Cuando registro un movimiento con descripción «Éxito»",
                "Entonces el sistema propone la categoría «Alimentación»",
                "Y la propuesta queda editable",
            ]),
            ("La clasificación no consume cuota", [
                "Dado que agoté mis registros asistidos del mes",
                "Cuando registro un gasto a mano",
                "Entonces el sistema igual me propone una categoría",
                "Y ningún contador de uso se incrementa",
            ]),
            ("Sin categoría clara", [
                "Cuando registro un movimiento cuya descripción no permite deducir la categoría",
                "Entonces el sistema deja el campo sin preseleccionar",
                "Y no elige una categoría al azar",
            ]),
        ],
    ),
    Historia(
        id="HU-21",
        titulo="Registrar un gasto con la foto del recibo",
        actividad="03", tarea="Capturar el movimiento", release="R3",
        rol="usuario",
        quiero="fotografiar un recibo y que el sistema extraiga los datos del movimiento",
        para="registrar lo que compré sin transcribir el papel",
        ru=["RU-01"], rf=["RF-17"], rn=["RN-19", "RN-23"], rnf=["RNF-01", "RNF-11"],
        escenarios=[
            ("Recibo legible", [
                "Cuando fotografío un recibo con total 87.500 del comercio «Farmatodo»",
                "Entonces el sistema propone un gasto de 87.500 con descripción «Farmatodo» y categoría «Salud»",
                "Y conserva la imagen asociada al movimiento",
            ]),
            ("Recibo ilegible", [
                "Cuando fotografío un recibo del que no puede extraerse el total",
                "Entonces el sistema me presenta el formulario con los campos que sí pudo derivar",
                "Y me pide completar el monto",
            ]),
            ("La imagen queda disponible en el historial", [
                "Dado que guardé un movimiento capturado por foto",
                "Cuando lo abro desde el historial",
                "Entonces puedo ver la imagen del recibo",
            ]),
        ],
    ),
    Historia(
        id="HU-22",
        titulo="Registrar aunque no tenga conexión",
        actividad="03", tarea="Capturar el movimiento", release="R3",
        rol="usuario sin conexión a internet",
        quiero="registrar un movimiento y que se sincronice cuando vuelva la señal",
        para="no perder el registro justo cuando estoy fuera de cobertura",
        ru=["RU-17"], rf=["RF-22"], rn=[], rnf=["RNF-16"],
        escenarios=[
            ("Registro sin conexión", [
                "Dado que mi dispositivo no tiene conexión",
                "Cuando registro un gasto de 20.000",
                "Entonces el movimiento queda guardado en el dispositivo",
                "Y el historial lo muestra señalado como pendiente de sincronizar",
            ]),
            ("Sincronización al recuperar la conexión", [
                "Dado que tengo dos movimientos pendientes de sincronizar",
                "Cuando el dispositivo recupera la conexión",
                "Entonces el sistema los envía automáticamente",
                "Y la marca de pendiente desaparece",
            ]),
            ("Los saldos locales reflejan lo pendiente", [
                "Dado que registré un gasto sin conexión",
                "Cuando consulto mi saldo neto en el dispositivo",
                "Entonces el gasto ya está descontado",
            ]),
        ],
        nota="La resolución de conflictos entre una edición local y una remota sobre el mismo movimiento aún no tiene regla de negocio definida: es la brecha que la matriz marca como cobertura **parcial** en RU-17.",
    ),
]
