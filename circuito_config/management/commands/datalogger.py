from django.core.management.base import BaseCommand, CommandError
from circuito_config.models import Parametro
import os

class Command(BaseCommand):
    help = 'Cron testing'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        #objetos = Parametro.objects.all().filter(ativo=True)

        #leitura do arquivo
        arquivo = open('/Users/robertopereira/Dropbox/ThermoGuardian/supervisorio-thermoguardian/src/supervisorio/log.txt', 'r', encoding="utf8")
        conteudo = arquivo.readlines()

        conteudo.append('teste')

        arquivo = open('/Users/robertopereira/Dropbox/ThermoGuardian/supervisorio-thermoguardian/src/supervisorio/log.txt', 'w', encoding="utf8")
        arquivo.writelines(conteudo)
        arquivo.close()


        print('Hello World de uma app Django!!!')