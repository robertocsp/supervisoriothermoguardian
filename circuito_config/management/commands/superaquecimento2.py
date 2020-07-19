from django.core.management.base import BaseCommand, CommandError
from circuito_config.models import Parametro, Datalog, Logerros, Modulo, Superaquecimentoconfig, Superaquecimentolog
from random import randint

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

            succao = randint(4, 12)

            '''
            try:
                modulo_succao = Modulo.objects.get(no_subordinate=superaquecimentoconfig.succao_no_subordinate)
                try:
                    parametro = Parametro.objects.get(modulo=modulo_succao, endereco=superaquecimentoconfig.succao_no_parametro)
                    try:
                        datalog_succao = Datalog.objects.filter(parametro=parametro).latest('datahora')
                        succao = datalog_succao.valor

                    except:
                        mensagem = 'calculo do superaquecimento - Datalog referente ao parametro ' + str(parametro.endereco) + ' do modulo ' + str(
                                parametro.modulo.no_subordinate) + ' referente a SUCCAO nao encontrado'
                        #erro = Logerros(cod='TG006', descricao=mensagem)
                        #erro.save()
                        print(mensagem)
                except:
                    mensagem = 'calculo do superaquecimento - modulo: ' + str(modulo_succao.no_subordinate) + 'parametro de número: ' + str(superaquecimentoconfig.succao_no_parametro) + ' referente a SUCCAO não encontrado'
                    # erro = Logerros(cod='TG005', descricao=mensagem)
                    # erro.save()
                    print(mensagem)
            except:
                mensagem = 'calculo do superaquecimento - modulo succao ' + str(superaquecimentoconfig.succao_no_subordinate) + ' não cadastrado'
                # erro = Logerros(cod='TG004', descricao=mensagem)
                # erro.save()
                print(mensagem)

            '''

            try:
                modulo_evaporacao = Modulo.objects.get(no_subordinate=superaquecimentoconfig.evaporacao_no_subordinate)
                try:
                    parametro = Parametro.objects.get(modulo=modulo_evaporacao,
                                                      endereco=superaquecimentoconfig.evaporacao_no_parametro)
                    try:
                        datalog_evaporacao = Datalog.objects.filter(parametro=parametro).latest('datahora')
                        evaporacao = datalog_evaporacao.valor

                    except:
                        mensagem = 'calculo do superaquecimento - Datalog referente ao parametro ' + str(
                            parametro.endereco) + ' do modulo ' + str(
                            parametro.modulo.no_subordinate) + ' referente a EVAPORACAO, nao encontrado'
                        erro = Logerros(cod='TG006', descricao=mensagem)
                        erro.save()
                        #print(mensagem)
                except:
                    mensagem = 'calculo do superaquecimento - modulo: ' + str(
                        modulo_evaporacao.no_subordinate) + 'parametro de número: ' + str(
                        superaquecimentoconfig.evaporacao_no_parametro) + ' referente a EVAPORACAO não encontrado'
                    erro = Logerros(cod='TG005', descricao=mensagem)
                    erro.save()
                    #print(mensagem)
            except:
                mensagem = 'calculo do superaquecimento - modulo succao ' + str(
                    superaquecimentoconfig.succao_no_subordinate) + ' não cadastrado'
                erro = Logerros(cod='TG004', descricao=mensagem)
                erro.save()
                #print(mensagem)

            resultado = succao - evaporacao
            #print('resultado do superaquecimento: ' + str(resultado))
            conformidade = False
            if resultado > superaquecimentoconfig.max_superaquecimento or resultado < superaquecimentoconfig.min_superaquecimento:
                conformidade = False
            else:
                conformidade = True

            superaquecimentolog = Superaquecimentolog(resultado=resultado, superaquecimento=conformidade, superaquecimentoconfig=superaquecimentoconfig)
            superaquecimentolog.save()