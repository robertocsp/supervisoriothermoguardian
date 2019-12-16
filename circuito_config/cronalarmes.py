from circuito_config.models import Parametro, Datalog, Logerros, Modulo, Alarme, Alarmelog
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings


def my_scheduled_job():
    def ultimo_registro_em_alarme(alarme, datalog):
        try:
            if Alarmelog.objects.filter(datalog=datalog).count() == 0:

                resultado = datalog.valor
                if resultado < alarme.minimo or resultado > alarme.maximo:
                    return 1, resultado
                else:
                    return 0, ''
            else:
                return 2, ''

        except:
            mensagem = 'Alarme - Datalog referente ao parametro ' + str(
                datalog.parametro.endereco) + ' do modulo ' + str(
                datalog.parametro.modulo.no_slave) + ' nao encontrado'
            erro = Logerros(cod='TG009', descricao=mensagem)
            erro.save()
            # print(mensagem)

    def sms_enviado_periodo(alarme):
        return True

    def email_enviado_periodo(alarme):
        if alarme.ultimo_email_enviado is not None:
            if alarme.ultimo_email_enviado < (timezone.now() - timedelta(hours=alarme.tempo_para_reenvio_email)):
                return False
            else:
                return True
        else:
            print('parece que o registro de data não é none, segue valor: ' + str(alarme.ultimo_email_enviado))
            return False

    def envia_sms():
        print('funcao que vai enviar sms')

    def envia_email(alarmelog):
        subject = 'ALARME: ' + alarmelog.alarme.nome
        message = 'Parametro fora dos valores determinados - Valor mínimo: ' + str(
            alarmelog.alarme.minimo) + ' Valo máximo: ' + str(alarmelog.alarme.maximo) + ' Valor registrado: ' + str(
            alarmelog.resultado)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['80.pereira@gmail.com', ]
        send_mail(subject, message, email_from, recipient_list)

    lista_alarmes = Alarme.objects.all()

    for alarme in lista_alarmes:
        try:
            modulo = Modulo.objects.get(no_slave=alarme.no_slave)
            try:
                parametro = Parametro.objects.get(modulo=modulo, endereco=alarme.no_parametro)

                datalog = Datalog.objects.filter(parametro=parametro).latest('datahora')

                retorno, resultado = ultimo_registro_em_alarme(alarme, datalog)

                # retorno = 0, saiu de alarme, retorno = 1, ainda em alarme, retorno = 2, mesmo datalog, não faz nada
                if retorno == 1:
                    # verifica se foi enviado email e sms no último periodo.
                    alarmelog = Alarmelog()
                    alarmelog.resultado = datalog.valor
                    alarmelog.datalog = datalog
                    alarmelog.alarme = alarme

                    if not sms_enviado_periodo(alarme):
                        envia_sms()
                        alarmelog.sms_enviado = True
                        alarme.ultimo_sms_enviado = timezone.now()

                    if not email_enviado_periodo(alarme):
                        envia_email(alarmelog)
                        alarmelog.email_enviado = True
                        alarme.ultimo_email_enviado = timezone.now()

                    alarmelog.save()
                    alarme.em_alarme = True
                    alarme.save()

                    print('salvou')


                elif retorno == 0:
                    print('remove o status de em_alarme')
            except:
                mensagem = 'Alarme - modulo: ' + str(alarme.no_slave) + ', parametro de número: ' + str(
                    alarme.no_parametro) + ' não encontrado'
                erro = Logerros(cod='TG008', descricao=mensagem)
                erro.save()
                # print(mensagem)
        except:
            mensagem = 'Alarme - modulo' + str(alarme.no_slave) + ' não encontrado'
            erro = Logerros(cod='TG007', descricao=mensagem)
            erro.save()
            print(mensagem)