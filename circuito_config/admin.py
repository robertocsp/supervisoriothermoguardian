from django.contrib import admin
from . import models


@admin.register(models.Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')



@admin.register(models.Datalog)
class DatalogAdmin(admin.ModelAdmin):
    list_display = ('valor', 'parametro_unidade', 'datahora','parametro', 'parametro_nome',)
    list_filter = (
        ('parametro__modulo__circuito__nome'),
        ('parametro__modulo__no_slave'),
        ('parametro__nome')
    )

    def parametro_nome(self, instance):
        return instance.parametro.nome

    def parametro_unidade(self, instance ):
        return instance.parametro.unidade


admin.site.register(models.Circuito)
admin.site.register(models.Modulo)
admin.site.register(models.Parametro)



