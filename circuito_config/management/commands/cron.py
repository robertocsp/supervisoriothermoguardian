from django.core.management.base import BaseCommand, CommandError
import os
from crontab import CronTab

class Command(BaseCommand):
    help = 'Cron testing'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        #init cron
        cron = CronTab(user='robertopereira')

        #add new cron job
        job = cron.new(command='python /Users/robertopereira/Dropbox/ThermoGuardian/supervisorio-thermoguardian/src/supervisorio/circuito_config/management/commands/datalogger.py')

        #job settings
        job.minute.every(1)

        cron.write()