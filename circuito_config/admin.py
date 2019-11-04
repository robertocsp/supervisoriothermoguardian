from django.contrib import admin
from . import models


class DatalogAdmin(admin.ModelAdmin):
    list_display = ('valor', 'parametro_unidade', 'datahora','parametro', 'parametro_nome',)

    def parametro_nome(self, instance):
        return instance.parametro.nome

    def parametro_unidade(self, instance ):
        return instance.parametro.unidade

admin.site.register(models.Circuito)
admin.site.register(models.Modulo)
admin.site.register(models.Parametro)
admin.site.register(models.Datalog, DatalogAdmin)


