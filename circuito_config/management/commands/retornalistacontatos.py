from django.core.management.base import BaseCommand, CommandError
from circuito_config.models import Parametro, Datalog, Logerros, Modulo, Alarme, Alarmelog, Contatosalarme

class Command(BaseCommand):
    help = 'Cron testing'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        lista_contatos = Contatosalarme.objects.filter(recebe_email=True)
        emails = []
        for contato in lista_contatos:
            emails.append(contato.email)

        print(emails)

