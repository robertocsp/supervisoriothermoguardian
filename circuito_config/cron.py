from circuito_config.models import Parametro, Datalog
import minimalmodbus


def my_scheduled_job():
    objetos = Parametro.objects.all().filter(ativo=True)

    for parametro in objetos:

        instrument = minimalmodbus.Instrument(parametro.modulo.porta, parametro.modulo.no_slave)  # port name, slave address (in decimal)

        instrument.serial.baudrate = parametro.modulo.baudrate  # Baud
        instrument.serial.parity = parametro.modulo.parity
        instrument.serial.bytesize = parametro.modulo.bytesize
        instrument.serial.stopbits = parametro.modulo.stopbits
        instrument.serial.timeout = parametro.modulo.timeout

        #tem que testar o parametro de tipo de dados para saber se faz a leitura com o
        #read_register ou com o read_long
        register = instrument.read_register(parametro.endereco)

        register = register / parametro.escala

        datalog = Datalog()
        datalog.parametro = parametro
        datalog.valor = register
        datalog.save()

        # leitura do arquivo
        arquivo = open('/Users/robertopereira/Dropbox/ThermoGuardian/supervisorio-thermoguardian/src/supervisorio/log.txt', 'r', encoding="utf8")
        conteudo = arquivo.readlines()

        conteudo.append(register + '\n')

        arquivo = open('/Users/robertopereira/Dropbox/ThermoGuardian/supervisorio-thermoguardian/src/supervisorio/log.txt', 'w', encoding="utf8")
        arquivo.writelines(conteudo)
        arquivo.close()

    print('hello world no django crontab')