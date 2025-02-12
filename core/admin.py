from django.contrib import admin
from .models import Agencia, Pix_agencia, Socio, Cliente, Conta, Periodo, Investimento, Retirada, Superusuario, \
    InvestimentoCartao, PrestacaoCartao
from django.contrib.auth.models import User

class SuperusuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'nome')
    search_fields = ('usuario__username', 'nome')
    list_filter = ('usuario',)

class AgenciaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data_criacao', 'cnpj', 'gerente')
    search_fields = ('nome', 'cnpj', 'gerente')
    list_filter = ('data_criacao',)

class PixAgenciaAdmin(admin.ModelAdmin):
    list_display = ('agencia', 'nome', 'banco', 'chave', 'cpf_cnpj')
    search_fields = ('agencia__nome', 'banco', 'chave')
    list_filter = ('agencia',)

class SocioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data_inicio', 'telefone', 'cpf', 'ativo')
    search_fields = ('nome', 'cpf', 'telefone')
    list_filter = ('ativo', 'data_inicio')

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data_nascimento', 'telefone', 'cpf', 'ativo')
    search_fields = ('nome', 'cpf', 'telefone')
    list_filter = ('ativo',)

class ContaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'agencia', 'cliente', 'socio', 'data_abertura', 'porcentagem')
    search_fields = ('agencia__nome', 'cliente__nome', 'socio__nome')
    list_filter = ('agencia', 'data_abertura')

class PeriodoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'data_inicio', 'data_fim', 'dinheiro', 'alavancagem', 'aberto')
    search_fields = ('cliente__nome',)
    list_filter = ('aberto', 'data_inicio', 'data_fim', 'dinheiro', 'alavancagem')

class InvestimentoAdmin(admin.ModelAdmin):
    list_display = ('periodo', 'socio', 'data_inicio', 'data_fim', 'valor', 'valor_rendimento', 'porcent_rend_valor', 'autorizado', 'data_solicitacao')
    search_fields = ('periodo__cliente__nome', 'socio__nome', 'valor', 'porcent_rend_valor')
    list_filter = ('autorizado', 'data_solicitacao')

class RetiradaAdmin(admin.ModelAdmin):
    list_display = ('periodo', 'data_solicitacao', 'data', 'valor', 'chave_pix', 'banco_pix', 'titular_pix', 'autorizado', 'autorizador')
    search_fields = ('periodo__cliente__nome', 'valor', 'chave_pix', 'titular_pix')
    list_filter = ('autorizado', 'data_solicitacao')

from django.utils.html import format_html

# Configuração do modelo InvestimentoCartao
class InvestimentoCartaoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cliente',
        'socio',
        'data_inicio',
        'data_fim',
        'valor_maquineta',
        'valor_real',
        'rendimento_total',
        'rendimento_mes',
        'porcent_rend_valor',
        'comprovante_link',  # Exibir o link do comprovante se houver
        'autorizador',
        'autorizado',
        'aberto'
    )
    list_filter = ('cliente', 'socio', 'autorizado', 'aberto')  # Filtros rápidos
    search_fields = ('id', 'cliente__nome', 'socio__nome')  # Busca pelos campos relevantes
    list_editable = ('autorizado', 'aberto')  # Campos que podem ser editados diretamente na listagem
    ordering = ('-data_inicio',)  # Ordena por data de início (mais recente primeiro)

    def comprovante_link(self, obj):
        if obj.comprovante:
            return format_html('<a href="{0}" target="_blank">Ver Comprovante</a>', obj.comprovante.url)
        return '-'
    comprovante_link.short_description = 'Comprovante'

# Configuração do modelo PrestacaoCartao
class PrestacaoCartaoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'investimento_cartao',
        'data',
        'valor',
        'autorizador',
        'autorizado',
        'confirmador_pagamento',
        'pago'
    )
    list_filter = ('investimento_cartao', 'autorizado', 'pago')  # Filtros rápidos
    search_fields = ('id', 'investimento_cartao__id', 'investimento_cartao__cliente__nome')
    list_editable = ('autorizado', 'pago')  # Campos que podem ser editados diretamente na listagem
    ordering = ('-data',)  # Ordena por data (mais recente primeiro)



# Registrando os modelos no admin do Django
admin.site.register(Superusuario, SuperusuarioAdmin)
admin.site.register(Agencia, AgenciaAdmin)
admin.site.register(Pix_agencia, PixAgenciaAdmin)
admin.site.register(Socio, SocioAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Conta, ContaAdmin)
admin.site.register(Periodo, PeriodoAdmin)
admin.site.register(Investimento, InvestimentoAdmin)
admin.site.register(Retirada, RetiradaAdmin)
admin.site.register(InvestimentoCartao, InvestimentoCartaoAdmin)
admin.site.register(PrestacaoCartao, PrestacaoCartaoAdmin)

