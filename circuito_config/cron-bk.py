from circuito_config.models import Parametro, Datalog, Logerros
import minimalmodbus


def my_scheduled_job():

    #Datalogger
    objetos = Parametro.objects.all().filter(ativo=True)

    for parametro in objetos:

        try:
            instrument = minimalmodbus.Instrument(parametro.modulo.circuito.porta,
                                                  parametro.modulo.no_slave)  # port name, slave address (in decimal)

            instrument.serial.baudrate = parametro.modulo.circuito.baudrate  # Baud
            instrument.serial.parity = parametro.modulo.circuito.parity
            instrument.serial.bytesize = parametro.modulo.circuito.bytesize
            instrument.serial.stopbits = parametro.modulo.circuito.stopbits
            instrument.serial.timeout = parametro.modulo.circuito.timeout

            # tem que testar o parametro de tipo de dados para saber se faz a leitura com o
            # read_register ou com o read_long

            try:
                if parametro.datatype == parametro.bits32:
                    if parametro.signed:
                        register = instrument.read_long(parametro.endereco, signed=True)
                    else:
                        register = instrument.read_long(parametro.endereco, signed=False)
                else:
                    if parametro.signed:
                        register = instrument.read_register(parametro.endereco, signed=True)
                    else:
                        register = instrument.read_register(parametro.endereco, signed=False)


                register = register / parametro.escala

                datalog = Datalog()
                datalog.parametro = parametro
                datalog.valor = register
                datalog.save()
            except:
                mensagem = 'parametro de endereco ' + str(parametro.endereco) + ' do modulo ' + str(parametro.modulo.no_slave) + ' nao encontrado'
                erro = Logerros(cod='TG001', descricao=mensagem)
                erro.save()
        except:
            mensagem = 'porta com endereço ' + str(parametro.modulo.circuito.porta) + ' não identificada'
            erro = Logerros(cod='TG002', descricao=mensagem)
            erro.save()
            break

    #Superaquecimento


    print('Cron Supervisorio excutado')

