from django.core.management.base import BaseCommand, CommandError
from circuito_config.models import Parametro, Datalog, Logerros, Modulo
import os
import minimalmodbus
import time


class Command(BaseCommand):
    help = 'Cron testing'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        lista_modulos = Modulo.objects.all()

        for modulo in lista_modulos:
            #print(modulo)
            try:
                instrument = minimalmodbus.Instrument(modulo.circuito.porta,
                                                      modulo.no_subordinate)  # port name, subordinate address (in decimal)

                instrument.serial.baudrate = modulo.circuito.baudrate  # Baud
                instrument.serial.parity = modulo.circuito.parity
                instrument.serial.bytesize = modulo.circuito.bytesize
                instrument.serial.stopbits = modulo.circuito.stopbits
                instrument.serial.timeout = modulo.circuito.timeout

                lista_parametros = Parametro.objects.filter(modulo=modulo)

                for parametro in lista_parametros:
                    #print(parametro.endereco)
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
                        time.sleep(0.5)
                        #print('leu parametro')

                    except:
                        mensagem = 'parametro de endereco ' + str(parametro.endereco) + ' do modulo ' + str(
                            parametro.modulo.no_subordinate) + ' nao encontrado'
                        erro = Logerros(cod='TG001', descricao=mensagem)
                        erro.save()
            except:
                mensagem = 'porta com endereço ' + str(modulo.circuito.porta) + ' incorreta'
                erro = Logerros(cod='TG002', descricao=mensagem)
                erro.save()
                #print(mensagem)
