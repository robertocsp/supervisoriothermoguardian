from circuito_config.models import Parametro, Datalog
import minimalmodbus


def my_scheduled_job():
    objetos = Parametro.objects.all().filter(ativo=True)

    for parametro in objetos:

        instrument = minimalmodbus.Instrument(parametro.modulo.circuito.porta,
                                              parametro.modulo.no_slave)  # port name, slave address (in decimal)

        instrument.serial.baudrate = parametro.modulo.circuito.baudrate  # Baud
        instrument.serial.parity = parametro.modulo.circuito.parity
        instrument.serial.bytesize = parametro.modulo.circuito.bytesize
        instrument.serial.stopbits = parametro.modulo.circuito.stopbits
        instrument.serial.timeout = parametro.modulo.circuito.timeout

        # tem que testar o parametro de tipo de dados para saber se faz a leitura com o
        # read_register ou com o read_long

        if parametro.datatype == parametro.bits32:
            register = instrument.read_long(parametro.endereco)
        else:
            register = instrument.read_register(parametro.endereco)

        register = register / parametro.escala

        datalog = Datalog()
        datalog.parametro = parametro
        datalog.valor = register
        datalog.save()

    print('Cron Supervisorio excutado')

