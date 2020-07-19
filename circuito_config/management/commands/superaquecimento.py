from django.core.management.base import BaseCommand, CommandError
from circuito_config.models import Parametro, Datalog, Logerros, Modulo, Superaquecimentoconfig, Superaquecimentolog
import os
import minimalmodbus


class Command(BaseCommand):
    help = 'Cron testing'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        lista_superaquecimento = Superaquecimentoconfig.objects.all()
        for superaquecimentoconfig in lista_superaquecimento:
            succao = 0
            evaporacao = 0
            try:
                modulo_succao = Modulo.objects.get(no_subordinate=superaquecimentoconfig.succao_no_subordinate)
                try:
                    instrument = minimalmodbus.Instrument(modulo_succao.circuito.porta,
                                                          modulo_succao.no_subordinate)  # port name, subordinate address (in decimal)

                    instrument.serial.baudrate = modulo_succao.circuito.baudrate  # Baud
                    instrument.serial.parity = modulo_succao.circuito.parity
                    instrument.serial.bytesize = modulo_succao.circuito.bytesize
                    instrument.serial.stopbits = modulo_succao.circuito.stopbits
                    instrument.serial.timeout = modulo_succao.circuito.timeout

                    try:
                        parametro = Parametro.objects.get(modulo=modulo_succao, endereco=superaquecimentoconfig.succao_no_parametro)

                        try:
                            if parametro.datatype == parametro.bits32:
                                if parametro.signed:
                                    succao = instrument.read_long(parametro.endereco, signed=True)
                                else:
                                    succao = instrument.read_long(parametro.endereco, signed=False)
                            else:
                                if parametro.signed:
                                    succao = instrument.read_register(parametro.endereco, signed=True)
                                else:
                                    succao = instrument.read_register(parametro.endereco, signed=False)

                            print('valor da succao: ' + str(succao))

                        except:
                            mensagem = 'calculo do superaquecimento - parametro de endereco ' + str(parametro.endereco) + ' do modulo ' + str(
                                parametro.modulo.no_subordinate) + ' nao encontrado'
                            #erro = Logerros(cod='TG006', descricao=mensagem)
                            #erro.save()
                            print(mensagem)

                    except:
                        mensagem = 'calculo do superaquecimento - modulo: ' + str(modulo_succao.no_subordinate) + 'parametro de número: ' + str(superaquecimentoconfig.succao_no_parametro) + ' referente a SUCCAO não encontrado'
                        # erro = Logerros(cod='TG005', descricao=mensagem)
                        # erro.save()
                        print(mensagem)
                except:
                    mensagem = 'calculo do superaquecimento - porta com endereço ' + str(modulo_succao.circuito.porta) + ' incorreta'
                    # erro = Logerros(cod='TG003', descricao=mensagem)
                    # erro.save()
                    print(mensagem)
            except:
                mensagem = 'calculo do superaquecimento - modulo succao ' + str(superaquecimentoconfig.succao_no_subordinate) + ' não cadastrado'
                # erro = Logerros(cod='TG004', descricao=mensagem)
                # erro.save()
                print(mensagem)

            try:
                modulo_evaporacao = Modulo.objects.get(no_subordinate=superaquecimentoconfig.evaporacao_no_subordinate)

                try:
                    instrument = minimalmodbus.Instrument(modulo_evaporacao.circuito.porta, modulo_evaporacao.no_subordinate)  # port name, subordinate address (in decimal)

                    instrument.serial.baudrate = modulo_evaporacao.circuito.baudrate  # Baud
                    instrument.serial.parity = modulo_evaporacao.circuito.parity
                    instrument.serial.bytesize = modulo_evaporacao.circuito.bytesize
                    instrument.serial.stopbits = modulo_evaporacao.circuito.stopbits
                    instrument.serial.timeout = modulo_evaporacao.circuito.timeout
                    try:
                        parametro = Parametro.objects.get(modulo=modulo_evaporacao, endereco=superaquecimentoconfig.evaporacao_no_parametro)

                        try:
                            if parametro.datatype == parametro.bits32:
                                if parametro.signed:
                                    evaporacao = instrument.read_long(parametro.endereco, signed=True)
                                else:
                                    evaporacao = instrument.read_long(parametro.endereco, signed=False)
                            else:
                                if parametro.signed:
                                    evaporacao = instrument.read_register(parametro.endereco, signed=True)
                                else:
                                    evaporacao = instrument.read_register(parametro.endereco, signed=False)

                            print('valor da evaporacao: ' + str(evaporacao))

                        except:
                            mensagem = 'calculo do superaquecimento - parametro de endereco ' + str(parametro.endereco) + ' do modulo ' + str(
                                parametro.modulo.no_subordinate) + 'referente a EVAPORACAO nao encontrado'
                            #erro = Logerros(cod='TG006', descricao=mensagem)
                            #erro.save()
                            print(mensagem)

                    except:
                        mensagem = 'calculo do superaquecimento - modulo: ' + str(modulo_evaporacao.no_subordinate) + 'parametro de número: ' + str(superaquecimentoconfig.evaporacao_no_parametro) + ' não encontrado'
                        # erro = Logerros(cod='TG005', descricao=mensagem)
                        # erro.save()
                        print(mensagem)
                except:
                    mensagem = 'calculo do superaquecimento - porta com endereço ' + str(modulo_evaporacao.circuito.porta) + ' incorreta'
                    # erro = Logerros(cod='TG003', descricao=mensagem)
                    # erro.save()
                    print(mensagem)
            except:
                mensagem = 'calculo do superaquecimento - modulo evaporacao ' + str(superaquecimentoconfig.evaporacao_no_subordinate) + ' não cadastrado'
                # erro = Logerros(cod='TG004', descricao=mensagem)
                # erro.save()
                print(mensagem)

            resultado = succao - evaporacao
            print('resultado do superaquecimento: ' + str(resultado))
            conformidade = False
            if resultado > superaquecimentoconfig.max_superaquecimento or resultado < superaquecimentoconfig.min_superaquecimento:
                conformidade = False
            else:
                conformidade = True

            superaquecimentolog = Superaquecimentolog(resultado=resultado, superaquecimento=conformidade, superaquecimentoconfig=superaquecimentoconfig)
            superaquecimentolog.save()

        print('fim do for')


