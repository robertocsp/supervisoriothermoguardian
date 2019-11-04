from django.core.management.base import BaseCommand, CommandError
from circuito_config.models import Parametro, Datalog
import os
import minimalmodbus

class Command(BaseCommand):
    help = 'Cron testing'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
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

            '''
            # leitura do arquivo
            arquivo = open(
                '/Users/robertopereira/Dropbox/ThermoGuardian/supervisorio-thermoguardian/src/supervisorio/log.txt',
                'r', encoding="utf8")
            conteudo = arquivo.readlines()

            conteudo.append(register + '\n')

            arquivo = open(
                '/Users/robertopereira/Dropbox/ThermoGuardian/supervisorio-thermoguardian/src/supervisorio/log.txt',
                'w', encoding="utf8")
            arquivo.writelines(conteudo)
            arquivo.close()
            '''