from django.core.management.base import BaseCommand, CommandError
from circuito_config.models import Parametro
import os

class Command(BaseCommand):
    help = 'Cron testing'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        objetos = Parametro.objects.all().filter(ativo=True)

        for parametro in objetos:

            print(parametro.bits32)