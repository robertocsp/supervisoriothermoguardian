# Generated by Django 2.2.6 on 2019-10-15 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('circuito_config', '0003_parametro_ativo'),
    ]

    operations = [
        migrations.AddField(
            model_name='parametro',
            name='nome',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
