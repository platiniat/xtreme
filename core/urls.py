from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),

    #clientes
    path('clientes/', views.cliente_list, name='cliente_list'),
    path('clientes/desativados', views.cliente_desativado_list, name='cliente_desativado_list'),
    path('clientes/novo/', views.cliente_create, name='cliente_create'),
    path('clientes/<int:pk>/editar/', views.cliente_edit, name='cliente_edit'),
    path('clientes/<int:pk>/desativar/', views.cliente_desative, name='cliente_desative'),
    path('clientes/<int:pk>/ativar/', views.cliente_ative, name='cliente_ative'),

    #agencias
    path('agencias/', views.agencia_list, name='agencia_list'),
    path('agencia/novo/', views.agencia_create, name='agencia_create'),
    path('agencia/<int:pk>/editar/', views.agencia_edit, name='agencia_edit'),
    path('agencia/<int:pk>/deletar/', views.agencia_delete, name='agencia_delete'),

    #pix
    path('agencia/<int:agencia_pk>/cahve-pix/criar', views.chave_pix_create, name='chave_pix_create'),
    path('chave-pix/<int:chave_pix_pk>/editar/', views.chave_pix_edit, name='chave_pix_edit'),
    path('chave-pix/<int:chave_pix_pk>/excluir/', views.chave_pix_delete, name='chave_pix_delete'),

    #socios
    path('socios/', views.socio_list, name='socio_list'),
    path('socio/novo/', views.socio_create, name='socio_create'),
    path('socio/<int:pk>/editar/', views.socio_edit, name='socio_edit'),
    path('socio/<int:pk>/deletar/', views.socio_delete, name='socio_delete'),

    #contas
    path('contas/<int:pk>/lista/', views.conta_list, name='conta_list'),
    path('conta/<int:pk>/novo/', views.conta_create, name='conta_create'),
    path('conta/<int:pk>/editar/', views.conta_edit, name='conta_edit'),

    #periodos (NOVO)
    path('periodo/<int:pk>/cliente/', views.periodo, name='periodo'),
    path('periodo-dinheiro/<int:pk>/criar/', views.periodo_dinheiro_create, name='periodo_dinheiro_create'),
    path('periodo-alavancagem/<int:pk>/criar/', views.periodo_alavancagem_create, name='periodo_alavancagem_create'),
    path('periodo-dinheiro/<int:pk>/lista/', views.periodo_dinheiro_list, name='periodo_dinheiro_list'),
    path('periodo-alavancagem/<int:pk>/lista/', views.periodo_alavancagem_list, name='periodo_alavancagem_list'),
    path('periodo/<int:pk>/investir-dinheiro/', views.investimento_dinheiro_create, name='investimento_dinheiro_create'),
    path('periodo/<int:pk>/investir-alavancagem/', views.investimento_alavancagem_create, name='investimento_alavancagem_create'),
    path('periodo/<int:pk>/investimento-dinheiro-editar/', views.investimento_dinheiro_edit, name='investimento_dinheiro_edit'),
    path('periodo/<int:pk>/investimento-dinheiro-excluir/', views.investimento_dinheiro_delete, name='investimento_dinheiro_delete'),
    path('periodo/<int:pk>/cadastrar-retirada/', views.retirada_create, name='retirada_create'),
    path('periodo/<int:pk>/retirada-editar/', views.retirada_edit, name='retirada_edit'),
    path('periodo/<int:pk>/retirada-excluir/', views.retirada_delete, name='retirada_delete'),
    path('periodo/<int:pk>/aprovar-solicitacao-aporte/', views.aprovar_solicitacao_aporte, name='aprovar_solicitacao_aporte'),
    path('periodo/<int:pk>/aprovar-solicitacao-rendimento/', views.aprovar_solicitacao_rendimento, name='aprovar_solicitacao_rendimento'),
    path('periodo/<int:pk>/investimento-cartao-finalizar/', views.investimento_cartao_finalizar, name='investimento_cartao_finalizar'),


    # area do investidor (NOVO)
    path('area-investidor/solicitacao-investimento/', views.solicitacao_investimento_create, name='solicitacao_investimento_create'),
    path('area-investidor/<int:pk>/solicitacao-investimento-editar/', views.solicitacao_investimento_edit, name='solicitacao_investimento_edit'),
    path('area-investidor/<int:pk>/solicitacao-investimento-excluir/', views.solicitacao_investimento_delete, name='solicitacao_investimento_delete'),
    path('area-investidor/solicitacao-retirada-rendimento/', views.solicitacao_retirada_rendimento_create, name='solicitacao_retirada_rendimento_create'),
    path('area-investidor/<int:pk>/solicitacao-retirada-rendimento-editar/', views.solicitacao_retirada_rendimento_edit, name='solicitacao_retirada_rendimento_edit'),
    path('area-investidor/<int:pk>/solicitacao-retirada-rendimento-excluir/', views.solicitacao_retirada_rendimento_delete, name='solicitacao_retirada_rendimento_delete'),


    #investimentos geral
    path('investimentos-lista/', views.investimento_list, name='investimento_list'),

    #retiradas geral
    path('retiradas-lista/', views.retirada_geral_list, name='retirada_geral_list'),

    path('investidor/<int:pk>/dinheiro-lista/', views.dinheiro_list, name='dinheiro_list'),

    path('investidor/<int:pk>/cartao-lista/', views.cartao_list, name='cartao_list'),
    path('investidor/<int:pk>/investir-cartao/', views.investimento_cartao_create, name='investimento_cartao_create'),
    path('investidor/<int:pk>/<int:periodo_pk>/investimento-cartao-editar/', views.investimento_cartao_edit, name='investimento_cartao_edit'),
    path('investidor/<int:pk>/investimento-cartao-excluir/', views.investimento_cartao_delete, name='investimento_cartao_delete'),
    path('investidor/cartao/<int:pk>/parcelas/', views.investimento_cartao_parcelas, name='investimento_cartao_parcelas'),
    path('investidor/cartao/<int:pk>/pagar-prestacao/', views.investimento_cartao_pagar_prestacao, name='investimento_cartao_pagar_prestacao'),
    path('investidor/cartao/<int:pk>/cancelar-prestacao/', views.investimento_cartao_cancelar_prestacao, name='investimento_cartao_cancelar_prestacao'),

    path('investidor/<int:pk>/alavancagem-lista/', views.alavancagem_list, name='alavancagem_list'),
    path('investidor/<int:pk>/investimento-alavancagem-editar/', views.investimento_alavancagem_edit, name='investimento_alavancagem_edit'),
    path('investidor/<int:pk>/investimento-alavancagem-excluir/', views.investimento_alavancagem_delete, name='investimento_alavancagem_delete'),

    path('investidor/<int:pk>/retirada-lista/', views.retirada_list, name='retirada_list'),

    path('investidor/<int:pk>/historico-investimentos/', views.investidor_investimento_list, name='investidor_investimento_list'),
    path('investidor/<int:pk>/historico-retiradas/', views.investidor_retirada_list, name='investidor_retirada_list'),
    path('investidor/<int:pk>/aprovar-solicitacao-retirada/', views.investidor_retirada_aprovar, name='investidor_retirada_aprovar'),

    path('investidor/<int:pk>/finalizar-periodo/', views.finalizar_periodo, name='finalizar_periodo'),
    path('investidor/<int:pk>/finalizar-periodo-novo/', views.finalizar_periodo_novo, name='finalizar_periodo_novo'),

    #novo investimentos anteriores
    path('investidor/<int:pk>/investimentos-anteriores-dinheiro/', views.investimentos_anteriores_dinheiro, name='investimentos_anteriores_dinheiro'),
    path('investidor/<int:pk>/investimentos-anteriores-cartao/', views.investimentos_anteriores_cartao, name='investimentos_anteriores_cartao'),

    #acesso do investidor ao sistema
    path('investidor/<int:pk>/acesso/', views.acesso_investidor, name='acesso_investidor'),
    path('investidor-area-index/', views.investidor_area_index, name='investidor_area_index'),
    path('investidor-area-investimentos/', views.investidor_area_investimentos, name='investidor_area_investimentos'),
    path('area-investidor/historico-investimentos/', views.area_investidor_investimento_list, name='area_investidor_investimento_list'),
    path('area-investidor/historico-retiradas/', views.area_investidor_retirada_list, name='area_investidor_retirada_list'),

    #dinheiro_investidor
    path('area-investidor/dinheiro-lista/', views.dinheiro_investidor_list, name='dinheiro_investidor_list'),

    #cartao_investidor
    path('area-investidor/cartao-lista/', views.cartao_investidor_list, name='cartao_investidor_list'),
    path('area-investidor/cartao/<int:pk>/parcelas/', views.investidor_area_cartao_parcelas, name='investidor_area_cartao_parcelas'),

    #alavancagem_investidor
    path('area-investidor/alavancagem-lista/', views.alavancagem_investidor_list, name='alavancagem_investidor_list'),

    #retirada_investidor
    path('area-investidor/retirada-lista/', views.retirada_investidor_list, name='retirada_investidor_list'),
    path('area-investidor/solicitar-retirada/', views.solicitar_retirada, name='solicitar_retirada'),


    #alterar senha
    path('alterar-senha/', views.alterar_senha, name='alterar_senha'),

    #marcar
    path('investidor/<int:pk>/marcar-investimento-reinvestir/', views.marcar_investimento_reinvestir, name='marcar_investimento_reinvestir'),
    path('investidor/<int:pk>/marcar-investimento-retirar/', views.marcar_investimento_retirar, name='marcar_investimento_retirar'),
    path('investidor/<int:pk>/limpar-marcacao-investimento/', views.limpar_marcacao_investimento, name='limpar_marcacao_investimento'),
    path('investidor/<int:pk>/marcar-rendimento-reinvestir/', views.marcar_rendimento_reinvestir, name='marcar_rendimento_reinvestir'),
    path('investidor/<int:pk>/marcar-rendimento-retirar/', views.marcar_rendimento_retirar, name='marcar_rendimento_retirar'),
    path('investidor/<int:pk>/limpar-marcacao-rendimento/', views.limpar_marcacao_rendimento, name='limpar_marcacao_rendimento'),

    path('investidor/<int:pk>/contrato/', views.contrato, name='contrato'),

]
