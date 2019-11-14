from django.contrib import admin
from . import models


@admin.register(models.Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')



@admin.register(models.Datalog)
class DatalogAdmin(admin.ModelAdmin):
    list_display = ('id', 'valor', 'parametro_unidade', 'datahora','parametro', 'parametro_nome',)
    list_filter = (
        ('parametro__modulo__circuito__nome'),
        ('parametro__modulo__no_slave'),
        ('parametro__nome')
    )

    def parametro_nome(self, instance):
        return instance.parametro.nome

    def parametro_unidade(self, instance ):
        return instance.parametro.unidade

@admin.register(models.Logerros)
class LogerrosAdmin(admin.ModelAdmin):
    list_display = ('cod', 'descricao', 'datahora')

@admin.register(models.Superaquecimentoconfig)
class SuperaquecimentoconfigAdmin(admin.ModelAdmin):
    list_display = ('nome', 'succao_no_slave', 'succao_no_parametro', 'evaporacao_no_slave', 'evaporacao_no_parametro', 'min_superaquecimento', 'max_superaquecimento')

@admin.register(models.Superaquecimentolog)
class SuperaquecimentologAdmin(admin.ModelAdmin):
    list_display = ('resultado', 'superaquecimento', 'superaquecimentoconfig', 'datahora')

admin.site.register(models.Circuito)
admin.site.register(models.Modulo)
admin.site.register(models.Parametro)



