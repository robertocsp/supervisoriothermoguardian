from django.core.management.base import BaseCommand, CommandError
from circuito_config.models import Parametro
import os

from django.utils import timezone
from datetime import datetime
from datetime import timedelta

class Command(BaseCommand):
    help = 'Cron testing'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        hora_alterada = timezone.now() + timedelta(hours=2)
        print(timezone.now())
        print(datetime.now())
        print(hora_alterada)
