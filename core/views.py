from calendar import monthrange
from datetime import datetime, date, timedelta

from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from core.models import *
from core.forms import *
from django.core.paginator import Paginator
from .models import *
from django.utils import timezone
from django.contrib.auth import update_session_auth_hash
import random
from django.contrib.auth import logout
from django.http import HttpResponse
import calendar
from datetime import timedelta


def verificar_socio(request):
    # Verifica se o usuário é Superusuario
    if Superusuario.objects.filter(usuario=request.user).exists():
        return True

    # Verifica se o usuário é Socio
    if Socio.objects.filter(usuario=request.user).exists():
        return True

    # Se o usuário não for Superusuario nem Socio, desloga e retorna False
    messages.error(request, 'Você não tem permissão para acessar esta página.')
    logout(request)
    return False

@login_required
def index(request):
    try:
        Superusuario.objects.get(usuario=request.user)
        return render(request, 'core/index.html')
    except:
        try:
            Socio.objects.get(usuario=request.user)
            return render(request, 'core/index.html')
        except:
            return redirect('investidor_area_index')

@login_required
def cliente_list(request):
    socio = verificar_socio(request)  # A função verifica se é socio, se nao for ele desloga e retorna False
    if not socio:
        return redirect('index')

    clientes = Cliente.objects.filter(ativo=True).order_by('nome')  # Ordena por nome

    # Defina a quantidade de itens por página
    itens_por_pagina = 100  # Ajuste conforme necessário

    paginator = Paginator(clientes, itens_por_pagina)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Lógica para limitar o número de páginas exibidas
    num_paginas_visiveis = 3
    metade_num_paginas_visiveis = num_paginas_visiveis // 2
    numero_da_pagina = page_obj.number
    num_total_de_paginas = paginator.num_pages

    inicio_paginacao = max(1, numero_da_pagina - metade_num_paginas_visiveis)
    final_paginacao = min(num_total_de_paginas, inicio_paginacao + num_paginas_visiveis - 1)

    if final_paginacao - inicio_paginacao + 1 < num_paginas_visiveis:
        inicio_paginacao = max(1, final_paginacao - num_paginas_visiveis + 1)

    paginas_visiveis = range(inicio_paginacao, final_paginacao + 1)

    return render(request, 'core/cliente_list.html', {
        'clientes': page_obj,
        'paginas_visiveis': paginas_visiveis,
    })

@login_required
def cliente_desativado_list(request):
    socio = verificar_socio(request)  # A função verifica se é socio, se nao for ele desloga e retorna False
    if not socio:
        return redirect('index')
    clientes = Cliente.objects.filter(ativo=False).order_by('nome')  # Ordena por nome

    # Defina a quantidade de itens por página
    itens_por_pagina = 100  # Ajuste conforme necessário

    paginator = Paginator(clientes, itens_por_pagina)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Lógica para limitar o número de páginas exibidas
    num_paginas_visiveis = 3
    metade_num_paginas_visiveis = num_paginas_visiveis // 2
    numero_da_pagina = page_obj.number
    num_total_de_paginas = paginator.num_pages

    inicio_paginacao = max(1, numero_da_pagina - metade_num_paginas_visiveis)
    final_paginacao = min(num_total_de_paginas, inicio_paginacao + num_paginas_visiveis - 1)

    if final_paginacao - inicio_paginacao + 1 < num_paginas_visiveis:
        inicio_paginacao = max(1, final_paginacao - num_paginas_visiveis + 1)

    paginas_visiveis = range(inicio_paginacao, final_paginacao + 1)

    return render(request, 'core/cliente_desativado_list.html', {
        'clientes': page_obj,
        'paginas_visiveis': paginas_visiveis,
    })

@login_required
def cliente_create(request):
    socio = verificar_socio(request)  # A função verifica se é socio, se nao for ele desloga e retorna False
    if not socio:
        return redirect('index')
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Investidor cadastrado com sucesso!')
            return redirect('cliente_list')  # Redireciona para a lista de clientes
    else:
        form = ClienteForm()

    return render(request, 'core/cliente_form.html', {'form': form})

@login_required
def cliente_edit(request, pk):
    socio = verificar_socio(request)  # A função verifica se é socio, se nao for ele desloga e retorna False
    if not socio:
        return redirect('index')
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Investidor atualizado com sucesso!')
            return redirect('cliente_list')  # Redireciona para a lista de clientes
    else:
        if(cliente.data_nascimento):
            cliente.data = cliente.data.strftime('%Y-%m-%d')
            cliente.data_nascimento = cliente.data_nascimento.strftime('%Y-%m-%d')
        if (cliente.data_nascimento_conjuge):
            cliente.data_nascimento_conjuge = cliente.data_nascimento_conjuge.strftime('%Y-%m-%d')
        form = ClienteForm(instance=cliente)

    return render(request, 'core/cliente_form.html', {'form': form, 'is_edit': True, 'cliente': cliente})

@login_required
def cliente_desative(request, pk):
    socio = verificar_socio(request)  # A função verifica se é socio, se nao for ele desloga e retorna False
    if not socio:
        return redirect('index')
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == 'POST':
        cliente.ativo = False
        cliente.save()
        messages.success(request, 'Investidor desativado com sucesso!')
        return redirect('cliente_list')  # Redireciona para a lista de clientes

    return render(request, 'core/cliente_desative_confirm.html', {'cliente': cliente})

@login_required
def cliente_ative(request, pk):
    socio = verificar_socio(request)  # A função verifica se é socio, se nao for ele desloga e retorna False
    if not socio:
        return redirect('index')
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == 'POST':
        cliente.ativo = True
        cliente.save()
        messages.success(request, 'Investidor ativado com sucesso!')
        return redirect('cliente_desativado_list')  # Redireciona para a lista de clientes

    return render(request, 'core/cliente_ative_confirm.html', {'cliente': cliente})

@login_required
def gerar_senha(request, pk):
    socio = verificar_socio(request)  # A função verifica se é socio, se nao for ele desloga e retorna False
    if not socio:
        return redirect('index')
    cliente = get_object_or_404(Cliente, pk=pk)

    # Gerar a nova senha
    letras = 'abcdefgh'
    numeros = '0123456789'
    nova_senha = ''.join(random.choices(letras, k=5)) + ''.join(random.choices(numeros, k=3))

    # Atualizar a senha do usuário associado
    if cliente.usuario:
        cliente.usuario.set_password(nova_senha)
        cliente.usuario.save()

    # Adicionar uma mensagem de sucesso
    messages.success(request, f'A nova senha é: {nova_senha}')

    # Redirecionar de volta para a página de edição
    return redirect('administrador_edit', pk=pk)

@login_required
def agencia_list(request):
    socio = verificar_socio(request)  # A função verifica se é socio, se nao for ele desloga e retorna False
    if not socio:
        return redirect('index')
    agencias = Agencia.objects.all().order_by('nome')
    return render(request, 'core/agencia_list.html', {'agencias':agencias})

@login_required
def agencia_create(request):
    socio = verificar_socio(request)  # A função verifica se é socio, se nao for ele desloga e retorna False
    if not socio:
        return redirect('index')
    if request.method == 'POST':
        form = AgenciaForm(request.POST)
        if form.is_valid():
            agencia = form.save(commit=False)
            agencia.numero = "00"+str(agencia.pk)
            agencia.save()
            messages.success(request, 'Agencia criada com sucesso!')
            return redirect('agencia_list')
    else:
        form = AgenciaForm()

    return render(request, 'core/agencia_form.html', {'form': form})

@login_required
def agencia_edit(request, pk):
    socio = verificar_socio(request)  # A função verifica se é socio, se nao for ele desloga e retorna False
    if not socio:
        return redirect('index')
    agencia = get_object_or_404(Agencia, pk=pk)

    if request.method == 'POST':
        form = AgenciaForm(request.POST, instance=agencia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Agencia alterada com sucesso!')
            return redirect('agencia_edit', pk)  # Redireciona para a lista de clientes
    else:
        form = AgenciaForm(instance=agencia)

    return render(request, 'core/agencia_form.html', {'form': form, 'is_edit': True, 'agencia': agencia})

@login_required
def agencia_delete(request, pk):
    socio = verificar_socio(request)  # A função verifica se é socio, se nao for ele desloga e retorna False
    if not socio:
        return redirect('index')
    agencia = get_object_or_404(Agencia, pk=pk)

    if request.method == 'POST':
        contas = Conta.objects.filter(agencia=agencia)
        if(len(contas) > 0):
            messages.warning(request, 'Agencia não pode ser deletada, pois existem contas relacionadas!')
            return redirect('agencia_edit', pk)
        else:
            agencia.delete()
            messages.success(request, 'Agencia excluida com sucesso!')
            return redirect('agencia_list')

    return render(request, 'core/agencia_confirm_delete.html', {'agencia': agencia})

@login_required
def chave_pix_create(request, agencia_pk):
    socio = verificar_socio(request)  # A função verifica se é socio, se nao for ele desloga e retorna False
    if not socio:
        return redirect('index')
    agencia = get_object_or_404(Agencia, pk=agencia_pk)

    if request.method == 'POST':
        form = PixAgenciaForm(request.POST)
        if form.is_valid():
            chave_pix = form.save(commit=False)
            chave_pix.agencia = agencia  # Associa a chave PIX à agência
            chave_pix.save()
            return redirect('agencia_edit', agencia.pk)  # Redireciona para o detalhe da agência
    else:
        form = PixAgenciaForm()

    return render(request, 'core/chave_pix_form.html', {'form': form, 'agencia': agencia})

@login_required
def chave_pix_edit(request, chave_pix_pk):
    socio = verificar_socio(request)  # A função verifica se é socio, se nao for ele desloga e retorna False
    if not socio:
        return redirect('index')
    # Recupera a chave PIX que será editada
    chave_pix = get_object_or_404(Pix_agencia, pk=chave_pix_pk)

    # Recupera a agência relacionada à chave PIX
    agencia = chave_pix.agencia

    if request.method == 'POST':
        form = PixAgenciaForm(request.POST, instance=chave_pix)
        if form.is_valid():
            form.save()
            return redirect('agencia_edit', agencia.pk)  # Redireciona para o detalhe da agência
    else:
        form = PixAgenciaForm(instance=chave_pix)

    return render(request, 'core/chave_pix_form.html', {'form': form, 'agencia': agencia, 'is_edit': True})


@login_required
def chave_pix_delete(request, chave_pix_pk):
    socio = verificar_socio(request)  # A função verifica se é socio, se nao for ele desloga e retorna False
    if not socio:
        return redirect('index')
    # Recupera a chave PIX que será excluída
    chave_pix = get_object_or_404(Pix_agencia, pk=chave_pix_pk)

    # Recupera a agência associada à chave PIX
    agencia = chave_pix.agencia

    if request.method == 'POST':
        # Exclui a chave PIX
        chave_pix.delete()
        # Exibe uma mensagem de sucesso
        messages.success(request, 'Chave PIX excluída com sucesso.')
        return redirect('agencia_edit', agencia.pk)  # Redireciona para a edição da agência

    return render(request, 'core/chave_pix_confirm_delete.html', {'chave_pix': chave_pix, 'agencia': agencia})

@login_required
def socio_list(request):
    socio = verificar_socio(request)  # A função verifica se é socio, se nao for ele desloga e retorna False
    if not socio:
        return redirect('index')
    socios = Socio.objects.all().order_by('nome')
    return render(request, 'core/socio_list.html', {'socios':socios})

@login_required
def socio_create(request):
    socio = verificar_socio(request)  # A função verifica se é socio, se nao for ele desloga e retorna False
    if not socio:
        return redirect('index')
    if request.method == 'POST':
        form = SocioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sócio criado com sucesso!')
            return redirect('socio_list')
    else:
        form = SocioForm()

    return render(request, 'core/socio_form.html', {'form': form})

@login_required
def socio_edit(request, pk):
    socio = verificar_socio(request)  # A função verifica se é socio, se nao for ele desloga e retorna False
    if not socio:
        return redirect('index')
    socio = get_object_or_404(Socio, pk=pk)

    if request.method == 'POST':
        form = SocioForm(request.POST, request.FILES, instance=socio)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sócio editado com sucesso!')
            return redirect('socio_edit', pk)  # Redireciona para a lista de clientes
    else:
        if(socio.data_inicio):
            socio.data_inicio = socio.data_inicio.strftime('%Y-%m-%d')
        form = SocioForm(instance=socio)

    return render(request, 'core/socio_form.html', {'form': form, 'is_edit': True, 'socio': socio})

@login_required
def socio_delete(request, pk):
    socio = verificar_socio(request)  # A função verifica se é socio, se nao for ele desloga e retorna False
    if not socio:
        return redirect('index')
    socio = get_object_or_404(Socio, pk=pk)

    if request.method == 'POST':
        contas = Conta.objects.filter(socio=socio)
        if(len(contas) > 0):
            messages.warning(request, 'Sócio não pode ser deletado, pois existem contas relacionadas!')
            return redirect('socio_edit', pk)
        else:
            socio.delete()
            messages.success(request, 'Sócio excluido com sucesso!')
            return redirect('socio_list')

    return render(request, 'core/socio_confirm_delete.html', {'socio': socio})


@login_required
def conta_list(request, pk):
    socio = verificar_socio(request)  # A função verifica se é socio, se nao for ele desloga e retorna False
    if not socio:
        return redirect('index')
    cliente = get_object_or_404(Cliente, pk=pk)
    contas = Conta.objects.filter(cliente=cliente)
    sem_conta = True
    conta=''
    if(len(contas) > 0):
        conta = contas[0]
        sem_conta = False

    return render(request, 'core/conta_list.html', {'cliente': cliente, 'contas':contas, 'sem_conta':sem_conta, 'conta':conta})

@login_required
def conta_create(request, pk):
    socio = verificar_socio(request)  # A função verifica se é socio, se nao for ele desloga e retorna False
    if not socio:
        return redirect('index')
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ContaForm(request.POST)
        if form.is_valid():
            conta = form.save(commit=False)
            conta.cliente = cliente
            conta.save()
            messages.success(request, 'Conta criada com sucesso!')
            return redirect('conta_list', conta.cliente.pk)
    else:
        form = ContaForm()

    return render(request, 'core/conta_form.html', {'form': form, 'cliente': cliente})


@login_required
def conta_edit(request, pk):
    socio = verificar_socio(request)  # A função verifica se é socio, se nao for ele desloga e retorna False
    if not socio:
        return redirect('index')
    conta = get_object_or_404(Conta, pk=pk)

    if request.method == 'POST':
        form = ContaForm(request.POST, instance=conta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta alterada com sucesso!')
            return redirect('conta_list', conta.cliente.pk)  # Redireciona para a lista de clientes
    else:
        conta.data_abertura = conta.data_abertura.strftime('%Y-%m-%d')
        form = ContaForm(instance=conta)

    return render(request, 'core/conta_form.html', {'form': form, 'is_edit': True, 'conta': conta, 'cliente':conta.cliente})


@login_required
def alterar_senha(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Atualiza a sessão do usuário para manter o login
            messages.success(request, 'Senha alterada com sucesso.')
            return redirect('index')  # Redireciona para a mesma página
        else:
            for error in form.errors.values():
                messages.warning(request, error)
    else:
        form = CustomPasswordChangeForm(request.user)

    context = {
        'form': form,
    }
    return render(request, 'core/alterar_senha.html', context)

@login_required
def periodo(request, pk):
    socio = verificar_socio(request)  # A função verifica se é socio, se nao for ele desloga e retorna False
    if not socio:
        return redirect('index')
    cliente = get_object_or_404(Cliente, pk=pk)
    # Tenta obter o período de dinheiro aberto
    periodo_dinheiro = Periodo.objects.filter(cliente=cliente, dinheiro=True, aberto=True).first()

    # Se não existir o periodo_dinheiro, cria um novo com base na data atual
    if not periodo_dinheiro:
        # Data atual
        hoje = timezone.now()
        # Primeiro dia do mês atual
        primeiro_dia_mes = hoje.replace(day=1)
        # Último dia do mês atual
        ultimo_dia_mes = hoje.replace(day=monthrange(hoje.year, hoje.month)[1])
        # Criação de um novo periodo
        periodo_dinheiro = Periodo.objects.create(
            cliente=cliente,
            dinheiro=True,
            aberto=True,
            data_inicio=primeiro_dia_mes,
            data_fim=ultimo_dia_mes
        )
    periodo_alavancagem = Periodo.objects.filter(cliente=cliente, alavancagem=True, aberto=True).first()
    cartoes_abertos = InvestimentoCartao.objects.filter(aberto=True, cliente=cliente)
    investimentos_anteriores_dinheiro = Investimento.objects.filter(periodo__cliente=cliente, periodo__aberto=False,autorizado=True, periodo__dinheiro=True).order_by('-data_inicio')
    ultimos_5_dinheiro = investimentos_anteriores_dinheiro[:5]
    if(len(investimentos_anteriores_dinheiro) > 5):
        maior_5_dinheiro = True
    else:
        maior_5_dinheiro = False
    investimentos_anteriores_cartao = InvestimentoCartao.objects.filter(cliente=cliente,aberto=False, autorizado=True).order_by('-data_inicio')
    ultimos_5_cartao = investimentos_anteriores_cartao[:5]
    if (len(investimentos_anteriores_cartao) > 5):
        maior_5_cartao = True
    else:
        maior_5_cartao = False
    return render(request, 'core/periodo.html', {'cliente': cliente, 'periodo_dinheiro':periodo_dinheiro,'periodo_alavancagem':periodo_alavancagem, 'cartoes_abertos':cartoes_abertos, 'ultimos_5_dinheiro': ultimos_5_dinheiro,'maior_5_dinheiro':maior_5_dinheiro,'ultimos_5_cartao': ultimos_5_cartao, 'maior_5_cartao': maior_5_cartao})


@login_required
def periodo_dinheiro_create(request, pk):
    socio = verificar_socio(request)  # A função verifica se é socio, se nao for ele desloga e retorna False
    if not socio:
        return redirect('index')
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == 'POST':
        form = PeriodoForm(request.POST)
        if form.is_valid():
            periodo = form.save(commit=False)
            periodo.cliente = cliente
            periodo.aberto = True  # Garantir que o novo período será aberto
            periodo.dinheiro = True
            periodo.alavancagem = False
            periodo.save()
            messages.success(request, 'Período criado com sucesso!')
            return redirect('periodo', pk=cliente.pk)  # Redireciona para a página do cliente
    else:
        form = PeriodoForm()
    return render(request, 'core/periodo_form.html', {'cliente':cliente, 'form':form})

@login_required
def periodo_alavancagem_create(request, pk):
    socio = verificar_socio(request)  # A função verifica se é socio, se nao for ele desloga e retorna False
    if not socio:
        return redirect('index')
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == 'POST':
        form = PeriodoForm(request.POST)
        if form.is_valid():
            periodo = form.save(commit=False)
            periodo.cliente = cliente
            periodo.aberto = True  # Garantir que o novo período será aberto
            periodo.dinheiro = False
            periodo.alavancagem = True
            periodo.save()
            messages.success(request, 'Período criado com sucesso!')
            return redirect('periodo', pk=cliente.pk)  # Redireciona para a página do cliente
    else:
        form = PeriodoForm()
    return render(request, 'core/periodo_form.html', {'cliente':cliente, 'form':form})

@login_required
def periodo_dinheiro_list(request, pk):
    socio = verificar_socio(request)  # A função verifica se é socio, se nao for ele desloga e retorna False
    if not socio:
        return redirect('index')
    periodo = get_object_or_404(Periodo, pk=pk)
    return render(request, 'core/periodo_dinheiro_list.html', {'periodo': periodo})

@login_required
def periodo_alavancagem_list(request, pk):
    socio = verificar_socio(request)  # A função verifica se é socio, se nao for ele desloga e retorna False
    if not socio:
        return redirect('index')
    periodo = get_object_or_404(Periodo, pk=pk)
    return render(request, 'core/periodo_alavancagem_list.html', {'periodo': periodo})


@login_required
def dinheiro_list(request, pk):
    socio = verificar_socio(request)  # A função verifica se é socio, se nao for ele desloga e retorna False
    if not socio:
        return redirect('index')
    cliente = get_object_or_404(Cliente, pk=pk)
    investimentos = Investimento.objects.filter(cliente=cliente, dinheiro=True,cartao=False,alavancagem=False, autorizado=True,finalizado=False)

    return render(request, 'core/dinheiro_list.html', {'cliente': cliente, 'investimentos':investimentos})

@login_required
def investimento_dinheiro_create(request, pk):
    socio = verificar_socio(request)
    if not socio:
        return redirect('index')
    periodo = get_object_or_404(Periodo, pk=pk)

    if request.method == 'POST':
        form = InvestimentoDinheiroForm(request.POST, user=request.user)

        if form.is_valid():
            investimento = form.save(commit=False)
            valor = investimento.valor
            porcent_rend_valor = investimento.porcent_rend_valor

            # Calcular rendimentos
            if porcent_rend_valor is not None and valor is not None:
                rendimentos = round((float(valor) * float(porcent_rend_valor)) / 100,2)
                investimento.valor_rendimento = rendimentos
            else:
                investimento.valor_rendimento = 0

            investimento.periodo = periodo
            investimento.autorizado = True
            investimento.autorizador = request.user
            investimento.reinvestido = False
            investimento.save()

            return redirect('periodo_dinheiro_list', pk)  # Redireciona para a lista de investimentos do cliente
        else:
            # Se o formulário não for válido, exibe a mensagem de erro
            messages.error(request, "Senha incorreta ou erro nos dados fornecidos.")
    else:
        form = InvestimentoDinheiroForm(user=request.user)

    return render(request, 'core/investimento_dinheiro_form.html', {'form': form, 'periodo': periodo})

@login_required
def investimento_dinheiro_edit(request, pk):
    socio = verificar_socio(request)
    if not socio:
        return redirect('index')

    try:
        investimento = Investimento.objects.get(pk=pk)
        periodo = investimento.periodo
    except Investimento.DoesNotExist:
        return HttpResponse("Investimento não encontrado.", status=404)

    if request.method == 'POST':
        form = InvestimentoDinheiroForm(request.POST, instance=investimento, user=request.user)

        if form.is_valid():
            investimento = form.save(commit=False)
            valor = investimento.valor
            porcent_rend_valor = investimento.porcent_rend_valor

            # Calcular rendimentos
            if porcent_rend_valor is not None and valor is not None:
                rendimentos = round((float(valor) * float(porcent_rend_valor)) / 100, 2)
                investimento.valor_rendimento = rendimentos
            else:
                investimento.valor_rendimento = 0

            investimento.periodo = periodo
            investimento.autorizado = True
            investimento.autorizador = request.user
            investimento.reinvestido = False
            investimento.save()

            return redirect('periodo_dinheiro_list', periodo.pk)  # Redireciona para a lista de investimentos do cliente
        else:
            # Se o formulário não for válido, exibe a mensagem de erro
            messages.error(request, "Senha incorreta ou erro nos dados fornecidos.")
    else:
        investimento.data_inicio = investimento.data_inicio.strftime('%Y-%m-%d')
        investimento.data_fim = investimento.data_fim.strftime('%Y-%m-%d')
        form = InvestimentoDinheiroForm(instance=investimento, user=request.user)

    return render(request, 'core/investimento_dinheiro_form.html', {'form': form, 'periodo': periodo})


@login_required
def investimento_dinheiro_delete(request, pk):
    # Verificar se o usuário é um sócio
    socio = verificar_socio(request)
    if not socio:
        return redirect('index')

    investimento = Investimento.objects.get(pk=pk)
    periodo = investimento.periodo

    # Se for um POST, verificar a senha do usuário
    if request.method == 'POST':
        senha = request.POST.get('senha')
        user = request.user

        # Verificar se a senha está correta
        if user.check_password(senha):
            investimento.delete()
            messages.success(request, "Investimento excluído com sucesso.")
            return redirect('periodo_dinheiro_list', periodo.pk)
        else:
            # Se a senha estiver incorreta, exibe a mensagem de erro
            messages.error(request, "Senha incorreta. Tente novamente.")

    return render(request, 'core/investimento_dinheiro_delete.html', {'investimento': investimento})


@login_required
def cartao_list(request, pk):
    socio = verificar_socio(request)  # A função verifica se é socio, se nao for ele desloga e retorna False
    if not socio:
        return redirect('index')
    cliente = get_object_or_404(Cliente, pk=pk)
    investimentos = Investimento.objects.filter(cliente=cliente, dinheiro=False,cartao=True,alavancagem=False)

    return render(request, 'core/cartao_list.html', {'cliente': cliente, 'investimentos':investimentos})

@login_required
def investimento_cartao_create(request, pk):
    socio = verificar_socio(request)
    if not socio:
        return redirect('index')

    try:
        periodo = Periodo.objects.get(pk=pk)
        cliente = periodo.cliente
    except Periodo.DoesNotExist:
        return HttpResponse("Periodo não encontrado.", status=404)

    if request.method == 'POST':
        senha = request.POST.get('senha')
        user = request.user

        # Verificar se a senha está correta
        if not user.check_password(senha):
            messages.error(request, "Senha incorreta. Tente novamente.")
            return redirect('periodo_dinheiro_list', periodo.pk)

        form = InvestimentoCartaoForm(request.POST)
        if form.is_valid():
            investimento = form.save(commit=False)
            investimento.cliente = cliente
            investimento.autorizado = True
            investimento.autorizador = request.user
            investimento.pago = False
            investimento.save()

            # Função para obter o último dia do mês
            def ultimo_dia_do_mes(data):
                ultimo_dia = calendar.monthrange(data.year, data.month)[1]
                return data.replace(day=ultimo_dia)

            # Lógica para criar as prestações apenas se o número de prestações for maior que zero
            num_prestacoes = investimento.num_prestacoes
            valor_parcela_cartao = investimento.valor_maquineta / num_prestacoes if num_prestacoes > 0 else 0
            rendimento_mes = investimento.valor_real * investimento.porcent_rend_valor / 100 if investimento.porcent_rend_valor > 0 else 0
            rendimento_total = rendimento_mes * num_prestacoes if investimento.porcent_rend_valor > 0 else 0

            investimento.valor_prestacao = round(valor_parcela_cartao,2)
            investimento.rendimento_total = rendimento_total
            investimento.rendimento_mes = rendimento_mes
            investimento.save()

            if num_prestacoes > 0:
                # Definir a data do primeiro rendimento como o último dia do mês da data de início
                data_vencimento = ultimo_dia_do_mes(investimento.data_inicio)

                # Criar o rendimento para cada parcela
                for i in range(num_prestacoes):
                    # Criar a prestação para o mês
                    PrestacaoCartao.objects.create(
                        investimento_cartao=investimento,
                        data=data_vencimento,  # Data do último dia do mês
                        autorizador=request.user,
                        valor=valor_parcela_cartao,

                    )

                    # Atualizar a data para o próximo mês
                    data_vencimento = ultimo_dia_do_mes(data_vencimento + relativedelta(months=1))  # Mover para o próximo mês
            messages.success(request, "Investimento cadastrado com sucesso.")
            return redirect('periodo_dinheiro_list', periodo.pk)
        else:
            # Se o formulário não for válido, exibe a mensagem de erro
            messages.error(request, "Erro ao processar o formulário. Verifique os dados.")
    else:
        form = InvestimentoCartaoForm()

    return render(request, 'core/investimento_cartao_form.html', {'form': form, 'cliente': cliente, 'periodo': periodo})

@login_required
def investimento_cartao_edit(request, pk, periodo_pk):
    socio = verificar_socio(request)
    if not socio:
        return redirect('index')

    try:
        investimento = InvestimentoCartao.objects.get(pk=pk)
        periodo = Periodo.objects.get(pk=periodo_pk)
        cliente = investimento.cliente
    except InvestimentoCartao.DoesNotExist:
        return HttpResponse("Investimento não encontrado.", status=404)

    if request.method == 'POST':
        senha = request.POST.get('senha')
        user = request.user

        # Verificar se a senha está correta
        if not user.check_password(senha):
            messages.error(request, "Senha incorreta. Tente novamente.")
            return redirect('investimento_cartao_edit', pk=pk)

        form = InvestimentoCartaoForm(request.POST, instance=investimento)
        if form.is_valid():
            num_prestacoes = form.cleaned_data['num_prestacoes']
            valor_maquineta = form.cleaned_data['valor_maquineta']
            valor_parcela_cartao = valor_maquineta / num_prestacoes if num_prestacoes > 0 else 0

            # Verificando se houve alteração no número de prestações ou no valor da maquineta
            if num_prestacoes != investimento.num_prestacoes or valor_maquineta != investimento.valor_maquineta:
                # Verificar se existem prestações pagas
                if PrestacaoCartao.objects.filter(investimento_cartao=investimento, pago=True).exists():
                    # Exibir mensagem informando que as prestações pagas serão excluídas
                    return render(request, 'core/investimento_cartao_confirmar_edicao.html', {'investimento': investimento})

            # Atualizar rendimento total e rendimento mensal
            rendimento_mes = investimento.valor_real * investimento.porcent_rend_valor / 100 if investimento.porcent_rend_valor > 0 else 0
            rendimento_total = rendimento_mes * num_prestacoes if investimento.porcent_rend_valor > 0 else 0

            # Salvar o investimento com os novos cálculos
            investimento = form.save(commit=False)
            investimento.valor_prestacao = round(valor_parcela_cartao, 2)
            investimento.rendimento_total = rendimento_total
            investimento.rendimento_mes = rendimento_mes
            investimento.save()

            # Função para obter o último dia do mês
            def ultimo_dia_do_mes(data):
                ultimo_dia = calendar.monthrange(data.year, data.month)[1]
                return data.replace(day=ultimo_dia)

            # Atualizar as prestações, caso necessário
            if num_prestacoes != investimento.num_prestacoes or valor_maquineta != investimento.valor_maquineta:
                # Excluir as prestações pagas
                PrestacaoCartao.objects.filter(investimento_cartao=investimento, pago=True).delete()

                # Recriar as prestações com os novos cálculos
                data_vencimento = ultimo_dia_do_mes(investimento.data_inicio)
                for i in range(num_prestacoes):
                    PrestacaoCartao.objects.create(
                        investimento_cartao=investimento,
                        data=data_vencimento,
                        autorizador=request.user,
                        valor=valor_parcela_cartao,
                    )
                    data_vencimento = ultimo_dia_do_mes(data_vencimento + relativedelta(months=1))

            messages.success(request, "Investimento editado com sucesso.")
            return redirect('periodo_dinheiro_list', periodo.pk)
        else:
            messages.error(request, "Erro ao processar o formulário. Verifique os dados.")
    else:
        investimento.data_inicio = investimento.data_inicio.strftime('%Y-%m-%d')
        investimento.data_fim = investimento.data_fim.strftime('%Y-%m-%d')
        form = InvestimentoCartaoForm(instance=investimento)

    return render(request, 'core/investimento_cartao_form.html', {'form': form, 'cliente': cliente, 'investimento': investimento})


@login_required
def investimento_cartao_delete(request, pk):
    # Verificar se o usuário é um sócio
    socio = verificar_socio(request)
    if not socio:
        return redirect('index')
    try:
        investimento = Investimento.objects.get(pk=pk)
        cliente = investimento.cliente
    except Investimento.DoesNotExist:
        return HttpResponse("Investimento não encontrado.", status=404)

    # Se for um POST, verificar a senha do usuário
    if request.method == 'POST':
        senha = request.POST.get('senha')
        user = request.user

        # Verificar se a senha está correta
        if user.check_password(senha):
            # Se a senha estiver correta, exclui o investimento
            rendimentos = Rendimento.objects.filter(investimento=investimento)
            for r in rendimentos:
                r.delete()
            investimento.delete()
            messages.success(request, "Investimento excluído com sucesso.")
            return redirect('cartao_list', pk=cliente.pk)
        else:
            # Se a senha estiver incorreta, exibe a mensagem de erro
            messages.error(request, "Senha incorreta. Tente novamente.")

    return render(request, 'core/investimento_cartao_delete.html', {'investimento': investimento})

@login_required
def investimento_cartao_parcelas(request, pk):
    # Verificar se o usuário é um sócio
    socio = verificar_socio(request)
    if not socio:
        return redirect('index')
    investimento = InvestimentoCartao.objects.get(pk=pk)
    cliente = investimento.cliente
    periodo = Periodo.objects.filter(cliente=cliente, dinheiro=True, aberto=True).first()

    return render(request, 'core/investimento_cartao_parcelas.html', {'investimento': investimento, 'periodo':periodo})


@login_required
def investimento_cartao_pagar_prestacao(request, pk):
    socio = verificar_socio(request)
    if not socio:
        return redirect('index')

    try:
        prestacao = PrestacaoCartao.objects.get(pk=pk)
    except PrestacaoCartao.DoesNotExist:
        return redirect('index')

    cliente = prestacao.investimento_cartao.cliente
    periodo = Periodo.objects.filter(cliente=cliente, dinheiro=True, aberto=True).first()

    if request.method == 'POST':
        senha_digitada = request.POST.get('senha')  # Pegando a senha digitada
        data_pagamento = request.POST.get('data_pagamento')  # Pegando a data digitada

        # Verifica se a senha está correta
        if senha_digitada:
            usuario = request.user
            if usuario.check_password(senha_digitada):  # Verifica a senha com a do usuário
                if data_pagamento:  # Se a data de pagamento foi informada
                    prestacao.data_pagamento = data_pagamento  # Atualiza a data de pagamento
                    prestacao.confirmador_pagamento = usuario
                    prestacao.cancelador_pagamento = None
                    prestacao.pago=True
                    prestacao.save()  # Salva a modificação
                    messages.success(request, "Pagamento realizado com sucesso.")
                    return redirect('investimento_cartao_parcelas', prestacao.investimento_cartao.pk)
                else:
                    messages.warning(request, "Data não informada.")
            else:
                messages.warning(request, "Senha incorreta.")
        else:
            messages.warning(request, "Por favor, digite sua senha.")

    return render(request, 'core/pagar_prestacao.html', {'prestacao': prestacao, 'periodo':periodo})

@login_required
def investimento_cartao_cancelar_prestacao(request, pk):
    socio = verificar_socio(request)
    if not socio:
        return redirect('index')

    try:
        prestacao = PrestacaoCartao.objects.get(pk=pk)
    except PrestacaoCartao.DoesNotExist:
        return redirect('index')

    cliente = prestacao.investimento_cartao.cliente
    periodo = Periodo.objects.filter(cliente=cliente, dinheiro=True, aberto=True).first()

    if request.method == 'POST':
        senha_digitada = request.POST.get('senha')  # Pegando a senha digitada

        # Verifica se a senha está correta
        if senha_digitada:
            usuario = request.user
            if usuario.check_password(senha_digitada):  # Verifica a senha com a do usuário
                prestacao.data_pagamento = None  # Atualiza a data de pagamento
                prestacao.pago=False
                prestacao.confirmador_pagamento = None
                prestacao.cancelador_pagamento = usuario
                prestacao.save()  # Salva a modificação
                messages.success(request, "Pagamento cancelado com sucesso.")
                return redirect('investimento_cartao_parcelas', prestacao.investimento_cartao.pk)
            else:
                messages.warning(request, "Senha incorreta.")
        else:
            messages.warning(request, "Por favor, digite sua senha.")

    return render(request, 'core/cancelar_prestacao.html', {'prestacao': prestacao, 'periodo':periodo})

@login_required
def alavancagem_list(request, pk):
    socio = verificar_socio(request)  # A função verifica se é socio, se nao for ele desloga e retorna False
    if not socio:
        return redirect('index')
    cliente = get_object_or_404(Cliente, pk=pk)
    investimentos = Investimento.objects.filter(cliente=cliente, dinheiro=False,cartao=False,alavancagem=True)

    return render(request, 'core/alavancagem_list.html', {'cliente': cliente, 'investimentos':investimentos})

@login_required
def investimento_alavancagem_create(request, pk):
    socio = verificar_socio(request)
    if not socio:
        return redirect('index')
    periodo = get_object_or_404(Periodo, pk=pk)

    if request.method == 'POST':
        form = InvestimentoAlavancagemForm(request.POST, user=request.user)

        if form.is_valid():
            investimento = form.save(commit=False)
            valor = investimento.valor
            porcent_rend_valor = investimento.porcent_rend_valor

            # Calcular rendimentos
            if porcent_rend_valor is not None and valor is not None:
                rendimentos = round((float(valor) * float(porcent_rend_valor)) / 100,2)
                investimento.valor_rendimento = rendimentos
            else:
                investimento.valor_rendimento = 0

            investimento.periodo = periodo
            investimento.autorizado = True
            investimento.autorizador = request.user
            investimento.reinvestido = False
            investimento.save()

            return redirect('periodo_alavancagem_list', pk)  # Redireciona para a lista de investimentos do cliente
        else:
            # Se o formulário não for válido, exibe a mensagem de erro
            messages.error(request, "Senha incorreta ou erro nos dados fornecidos.")
    else:
        form = InvestimentoDinheiroForm(user=request.user)

    return render(request, 'core/investimento_alavancagem_form.html', {'form': form, 'periodo': periodo})

@login_required
def investimento_alavancagem_edit(request, pk):
    socio = verificar_socio(request)
    if not socio:
        return redirect('index')

    try:
        investimento = Investimento.objects.get(pk=pk)
        periodo = investimento.periodo
    except Investimento.DoesNotExist:
        return HttpResponse("Investimento não encontrado.", status=404)

    if request.method == 'POST':
        form = InvestimentoAlavancagemForm(request.POST, instance=investimento, user=request.user)

        if form.is_valid():
            investimento = form.save(commit=False)
            valor = investimento.valor
            porcent_rend_valor = investimento.porcent_rend_valor

            # Calcular rendimentos
            if porcent_rend_valor is not None and valor is not None:
                rendimentos = round((float(valor) * float(porcent_rend_valor)) / 100, 2)
                investimento.valor_rendimento = rendimentos
            else:
                investimento.valor_rendimento = 0

            investimento.periodo = periodo
            investimento.autorizado = True
            investimento.autorizador = request.user
            investimento.reinvestido = False
            investimento.save()

            return redirect('periodo_alavancagem_list', periodo.pk)  # Redireciona para a lista de investimentos do cliente
        else:
            # Se o formulário não for válido, exibe a mensagem de erro
            messages.error(request, "Senha incorreta ou erro nos dados fornecidos.")
    else:
        investimento.data_inicio = investimento.data_inicio.strftime('%Y-%m-%d')
        investimento.data_fim = investimento.data_fim.strftime('%Y-%m-%d')
        form = InvestimentoDinheiroForm(instance=investimento, user=request.user)

    return render(request, 'core/investimento_alavancagem_form.html', {'form': form, 'periodo': periodo})


@login_required
def investimento_alavancagem_delete(request, pk):
    # Verificar se o usuário é um sócio
    socio = verificar_socio(request)
    if not socio:
        return redirect('index')

    investimento = Investimento.objects.get(pk=pk)
    periodo = investimento.periodo

    # Se for um POST, verificar a senha do usuário
    if request.method == 'POST':
        senha = request.POST.get('senha')
        user = request.user

        # Verificar se a senha está correta
        if user.check_password(senha):
            investimento.delete()
            messages.success(request, "Investimento excluído com sucesso.")
            return redirect('periodo_alavancagem_list', periodo.pk)
        else:
            # Se a senha estiver incorreta, exibe a mensagem de erro
            messages.error(request, "Senha incorreta. Tente novamente.")

    return render(request, 'core/investimento_alavancagem_delete.html', {'investimento': investimento})

@login_required
def retirada_list(request, pk):
    socio = verificar_socio(request)  # A função verifica se é socio ou super, se nao for ele desloga e retorna False
    if not socio:
        return redirect('index')
    cliente = get_object_or_404(Cliente, pk=pk)
    solicitacoes = Retirada.objects.filter(cliente=cliente, aprovado=False, finalizado=False)
    retiradas = Retirada.objects.filter(cliente=cliente, aprovado=True, finalizado=False)

    return render(request, 'core/retirada_list.html', {'cliente': cliente,'solicitacoes':solicitacoes, 'retiradas':retiradas})

@login_required
def retirada_create(request, pk):
    socio = verificar_socio(request)
    if not socio:
        return redirect('index')
    try:
        periodo = Periodo.objects.get(pk=pk)
    except Periodo.DoesNotExist:
        return HttpResponse("Periodo não encontrado.", status=404)

    disponivel = float(periodo.rendimento_disponivel_retirada())

    # Formatação do número pra enviar a quantidade disponivel
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    disponivel_formatado = locale.format_string("%.2f", disponivel, grouping=True)

    if request.method == 'POST':
        form = RetiradaForm(request.POST, request.FILES, user=request.user)

        if form.is_valid():
            valor = form.cleaned_data['valor']
            if(valor > disponivel):
                messages.warning(request, "ERRO AO TENTAR RETIRAR! R$"+str(disponivel)+" é o valor máximo!")
                return redirect('retirada_create', pk)
            else:
                retirada = form.save(commit=False)
                retirada.periodo = periodo
                retirada.autorizado = True
                retirada.autorizador = request.user
                retirada.save()

            return redirect('periodo_dinheiro_list', periodo.pk)
        else:
            # Se o formulário não for válido, exibe a mensagem de erro
            messages.error(request, "Senha incorreta ou erro nos dados fornecidos.")
    else:
        form = RetiradaForm(user=request.user,)

    return render(request, 'core/retirada_form.html', {'form': form, 'periodo': periodo, 'disponivel': disponivel_formatado})

@login_required
def retirada_edit(request, pk):
    socio = verificar_socio(request)
    if not socio:
        return redirect('index')
    try:
        retirada = Retirada.objects.get(pk=pk)
        periodo = retirada.periodo
    except Investimento.DoesNotExist:
        return HttpResponse("Retirada não encontrada.", status=404)

    disponivel = float(periodo.rendimento_disponivel_retirada())

    # Formatação do número pra enviar a quantidade disponivel
    disponivel_editar = round(float(disponivel) + float(retirada.valor),2)
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    disponivel_formatado = locale.format_string("%.2f", disponivel_editar, grouping=True)

    if request.method == 'POST':
        form = RetiradaForm(request.POST, request.FILES, instance=retirada,user=request.user)

        if form.is_valid():
            valor = form.cleaned_data['valor']
            if (valor > disponivel_editar):
                messages.warning(request, "ERRO AO TENTAR RETIRAR! R$" + str(disponivel_editar) + " é o valor máximo!")
                return redirect('retirada_edit', pk)
            else:
                retirada = form.save(commit=False)
                retirada.periodo = periodo
                retirada.autorizado = True
                retirada.autorizador = request.user
                retirada.save()

            return redirect('periodo_dinheiro_list', periodo.pk)
        else:
            # Se o formulário não for válido, exibe a mensagem de erro
            messages.error(request, "Senha incorreta ou erro nos dados fornecidos.")
    else:
        if(retirada.data):
            retirada.data = retirada.data.strftime('%Y-%m-%d')
        if (retirada.data_solicitacao):
            retirada.data_solicitacao = retirada.data_solicitacao.strftime('%Y-%m-%d')
        form = RetiradaForm(instance=retirada, user=request.user)

    return render(request, 'core/retirada_form.html', {'form': form, 'periodo': periodo, 'disponivel':disponivel_formatado})

@login_required
def retirada_delete(request, pk):
    # Verificar se o usuário é um sócio
    socio = verificar_socio(request)
    if not socio:
        return redirect('index')
    try:
        retirada = Retirada.objects.get(pk=pk)
        periodo = retirada.periodo
    except Retirada.DoesNotExist:
        return HttpResponse("Retirada não encontrada.", status=404)

    # Se for um POST, verificar a senha do usuário
    if request.method == 'POST':
        senha = request.POST.get('senha')
        user = request.user

        # Verificar se a senha está correta
        if user.check_password(senha):
            retirada.delete()
            messages.success(request, "Retirada excluída com sucesso.")
            return redirect('periodo_dinheiro_list', periodo.pk)
        else:
            # Se a senha estiver incorreta, exibe a mensagem de erro
            messages.error(request, "Senha incorreta. Tente novamente.")

    return render(request, 'core/retirada_delete.html', {'retirada': retirada})

@login_required
def investidor_retirada_aprovar(request, pk):
    # Verificar se o usuário é um sócio
    socio = verificar_socio(request)
    if not socio:
        return redirect('index')
    try:
        retirada = Retirada.objects.get(pk=pk)
        cliente = retirada.cliente
    except Retirada.DoesNotExist:
        return HttpResponse("Retirada não encontrada.", status=404)

    # Se for um POST, verificar a senha do usuário
    if request.method == 'POST':
        senha = request.POST.get('senha')
        data_retirada = request.POST.get('data_retirada')
        user = request.user

        # Verificar se a senha está correta
        if user.check_password(senha):
            retirada.aprovado = True
            retirada.aprovador = user
            retirada.data_retirada = data_retirada
            retirada.save()
            messages.success(request, "Solicitação confirmada com sucesso.")
            return redirect('retirada_list', pk=cliente.pk)
        else:
            # Se a senha estiver incorreta, exibe a mensagem de erro
            messages.error(request, "Senha incorreta. Tente novamente.")

    return render(request, 'core/investidor_retirada_aprovar.html', {'retirada': retirada})

@login_required
def acesso_investidor(request, pk):
    # Verificar se o usuário é um sócio
    socio = verificar_socio(request)
    if not socio:
        return redirect('index')

    data = {}
    investidor = get_object_or_404(Cliente, pk=pk)
    data['investidor'] = investidor

    if request.method == 'POST':
        usuario_nome = request.POST.get('usuario_nome', '').strip()

        # Verificar se o nome de usuário é válido
        if not usuario_nome:
            messages.warning(request, "O nome de usuário não pode estar vazio.")
        elif User.objects.filter(username=usuario_nome).exists() and (not investidor.usuario or investidor.usuario.username != usuario_nome):
            messages.warning(request, "Este nome de usuário já está em uso.")
        else:
            # Gerar a nova senha
            letras = 'abcdefgh'
            numeros = '0123456789'
            nova_senha = ''.join(random.choices(letras, k=5)) + ''.join(random.choices(numeros, k=3))

            # Verificar se o investidor já tem um usuário associado
            if investidor.usuario:
                # Se o nome de usuário for o mesmo, apenas atualiza a senha
                if investidor.usuario.username == usuario_nome:
                    investidor.usuario.set_password(nova_senha)
                    investidor.usuario.save()
                    messages.success(request, f'A senha foi atualizada com sucesso. A nova senha é: {nova_senha}')
                else:
                    # Caso o nome de usuário seja diferente, atualizar o nome e a senha
                    investidor.usuario.username = usuario_nome
                    investidor.usuario.set_password(nova_senha)
                    investidor.usuario.save()
                    messages.success(request, f'O nome de usuário foi atualizado. A nova senha é: {nova_senha}')
            else:
                # Criar um novo usuário para o investidor
                usuario = User.objects.create_user(username=usuario_nome, password=nova_senha)
                investidor.usuario = usuario
                investidor.save()
                messages.success(request, f'O nome de usuário foi criado. A nova senha é: {nova_senha}')

    return render(request, 'core/acesso_investidor.html', data)

@login_required
def finalizar_periodo(request, pk):
    # Verificar se o usuário é um sócio
    socio = verificar_socio(request)
    if not socio:
        return redirect('index')

    data = {}
    investidor = get_object_or_404(Cliente, pk=pk)
    data['investidor'] = investidor
    data['conta'] = Conta.objects.filter(cliente=investidor)[0]

    if request.method == 'POST':
        form = FinalizarPeriodoForm(request.POST)

        # Verifica a senha do administrador
        if form.is_valid():
            senha_administrador = form.cleaned_data['senha_administrador']
            if not request.user.check_password(senha_administrador):
                messages.warning(request, "Senha do administrador incorreta.")
                return redirect('finalizar_periodo', pk)  # Pode redirecionar para a mesma página ou outra

            # Recupera os dados do formulário
            data_inicio = form.cleaned_data['data_inicio']
            data_fim = form.cleaned_data['data_fim']
            porcentagem_rendimentos = form.cleaned_data['porcentagem_rendimentos']
            socio = form.cleaned_data['socio']

            conta = Conta.objects.filter(cliente=investidor)[0]
            valor_reinvestir = conta.valor_reinvestir()
            valor_formatado = valor_reinvestir.replace('.', '').replace(',', '.')
            valor_reinvestir = float(valor_formatado)

            investimentos = Investimento.objects.filter(
                cliente=investidor,
                dinheiro=True,
                autorizado=True
            )
            for i in investimentos:
                i.finalizado=True
                i.save()

            hoje = datetime.now()
            rendimentos_andamento = Rendimento.objects.filter(
                investimento__cliente=investidor,
                data__year__lte=hoje.year,
                data__month__lte=hoje.month,
                investimento__alavancagem=False,
                ativo=True
            )
            for r in rendimentos_andamento:
                r.ativo = False
                r.save()

            hoje = datetime.now()
            retiradas = Retirada.objects.filter(
                cliente=investidor,
                aprovado=True,
                finalizado=False
            )
            if(len(retiradas)>0):
                for r in retiradas:
                    r.finalizado=True
                    r.save()

            investimento_novo = Investimento.objects.create(
                cliente=investidor,
                socio=socio,
                data_inicio=data_inicio,
                data_fim=data_fim,
                valor=valor_reinvestir,
                porcent_rend_valor=porcentagem_rendimentos,
                dinheiro=True,
                reinvestido=True,
                autorizado=True
            )

            rendimento = float(valor_reinvestir) * float(porcentagem_rendimentos)
            rendimento = round(rendimento,2) / 100

            Rendimento.objects.create(
                investimento=investimento_novo,
                data=data_fim,
                valor=round(rendimento,2)
            )


            # Emite uma mensagem de sucesso (opcional)
            messages.success(request, "Formulário enviado com sucesso!")
            return redirect('conta_list', pk)  # Pode redirecionar para outra página

    else:
        form = FinalizarPeriodoForm()
    data['form'] = form


    return render(request, 'core/finalizar_periodo.html', data)

@login_required
def investidor_investimento_list(request, pk):
    # Verificar se o usuário é um sócio
    socio = verificar_socio(request)
    if not socio:
        return redirect('index')

    investidor = get_object_or_404(Cliente, pk=pk)
    investimentos = Investimento.objects.filter(cliente=investidor).order_by('finalizado', '-data_inicio')

    # Defina a quantidade de itens por página
    itens_por_pagina = 100  # Ajuste conforme necessário

    paginator = Paginator(investimentos, itens_por_pagina)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Lógica para limitar o número de páginas exibidas
    num_paginas_visiveis = 3
    metade_num_paginas_visiveis = num_paginas_visiveis // 2
    numero_da_pagina = page_obj.number
    num_total_de_paginas = paginator.num_pages

    inicio_paginacao = max(1, numero_da_pagina - metade_num_paginas_visiveis)
    final_paginacao = min(num_total_de_paginas, inicio_paginacao + num_paginas_visiveis - 1)

    if final_paginacao - inicio_paginacao + 1 < num_paginas_visiveis:
        inicio_paginacao = max(1, final_paginacao - num_paginas_visiveis + 1)

    paginas_visiveis = range(inicio_paginacao, final_paginacao + 1)

    return render(request, 'core/investidor_investimento_list.html', {
        'investidor': investidor,
        'investimentos': page_obj,
        'paginas_visiveis': paginas_visiveis,
    })

@login_required
def investidor_retirada_list(request, pk):
    # Verificar se o usuário é um sócio
    socio = verificar_socio(request)
    if not socio:
        return redirect('index')

    investidor = get_object_or_404(Cliente, pk=pk)
    retiradas = Retirada.objects.filter(cliente=investidor).order_by('-aprovado','-data_retirada')

    # Defina a quantidade de itens por página
    itens_por_pagina = 100  # Ajuste conforme necessário

    paginator = Paginator(retiradas, itens_por_pagina)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Lógica para limitar o número de páginas exibidas
    num_paginas_visiveis = 3
    metade_num_paginas_visiveis = num_paginas_visiveis // 2
    numero_da_pagina = page_obj.number
    num_total_de_paginas = paginator.num_pages

    inicio_paginacao = max(1, numero_da_pagina - metade_num_paginas_visiveis)
    final_paginacao = min(num_total_de_paginas, inicio_paginacao + num_paginas_visiveis - 1)

    if final_paginacao - inicio_paginacao + 1 < num_paginas_visiveis:
        inicio_paginacao = max(1, final_paginacao - num_paginas_visiveis + 1)

    paginas_visiveis = range(inicio_paginacao, final_paginacao + 1)

    return render(request, 'core/investidor_retirada_list.html', {
        'investidor': investidor,
        'retiradas': page_obj,
        'paginas_visiveis': paginas_visiveis,
    })

@login_required
def investidor_area_index(request):
    usuario = request.user
    investidor = Cliente.objects.get(usuario=usuario)
    return render(request, 'core/investidor_area_index.html', {'investidor':investidor})

@login_required
def investidor_area_investimentos(request):
    usuario = request.user
    cliente = Cliente.objects.get(usuario=usuario)
    periodo_dinheiro = Periodo.objects.filter(cliente=cliente, dinheiro=True, aberto=True).first()
    periodo_alavancagem = Periodo.objects.filter(cliente=cliente, alavancagem=True, aberto=True).first()
    cartoes_abertos = InvestimentoCartao.objects.filter(aberto=True, cliente=cliente)
    solicitacoes_investimentos = Investimento.objects.filter(periodo=periodo_dinheiro,autorizado=False)
    solicitacoes_retiradas_rendimentos = Retirada.objects.filter(periodo=periodo_dinheiro, autorizado=False)
    return render(request, 'core/investidor_area_investimentos.html', {'cliente':cliente, 'periodo_dinheiro':periodo_dinheiro, 'periodo_alavancagem':periodo_alavancagem,'cartoes_abertos':cartoes_abertos, 'solicitacoes_investimentos':solicitacoes_investimentos, 'solicitacoes_retiradas_rendimentos':solicitacoes_retiradas_rendimentos})

@login_required
def dinheiro_investidor_list(request):
    usuario = request.user
    cliente = Cliente.objects.get(usuario=usuario)
    investimentos = Investimento.objects.filter(cliente=cliente, dinheiro=True,cartao=False,alavancagem=False, autorizado=True,finalizado=False)
    return render(request, 'core/dinheiro_investidor_list.html', {'cliente': cliente, 'investimentos':investimentos})

@login_required
def cartao_investidor_list(request):
    usuario = request.user
    cliente = Cliente.objects.get(usuario=usuario)
    investimentos = Investimento.objects.filter(cliente=cliente, dinheiro=False,cartao=True,alavancagem=False)

    return render(request, 'core/cartao_investidor_list.html', {'cliente': cliente, 'investimentos':investimentos})

@login_required
def alavancagem_investidor_list(request):
    usuario = request.user
    cliente = Cliente.objects.get(usuario=usuario)
    investimentos = Investimento.objects.filter(cliente=cliente, dinheiro=False,cartao=False,alavancagem=True)

    return render(request, 'core/alavancagem_investidor_list.html', {'cliente': cliente, 'investimentos':investimentos})

@login_required
def retirada_investidor_list(request):
    usuario = request.user
    cliente = Cliente.objects.get(usuario=usuario)
    solicitacoes = Retirada.objects.filter(cliente=cliente, aprovado=False, finalizado=False)
    retiradas = Retirada.objects.filter(cliente=cliente, aprovado=True, finalizado=False)

    return render(request, 'core/retirada_investidor_list.html', {'cliente': cliente,'solicitacoes':solicitacoes, 'retiradas':retiradas})


@login_required
def solicitar_retirada(request):
    usuario = request.user
    cliente = Cliente.objects.get(usuario=usuario)

    hoje = datetime.now()
    total_rendimentos_andamento = Rendimento.objects.filter(
        investimento__cliente=cliente,
        data__year__lte=hoje.year,
        data__month__lte=hoje.month,
        investimento__alavancagem=False,
        ativo=True
    ).aggregate(Sum('valor'))
    soma_rendimentos = total_rendimentos_andamento['valor__sum'] or 0.0
    soma = round(soma_rendimentos)

    retiradas = Retirada.objects.filter(
        cliente=cliente,
        #aprovado=True,
        finalizado=False
    ).aggregate(Sum('valor'))

    # Obtemos a soma e verificamos se é None
    soma = retiradas.get('valor__sum', 0.0)

    # Se a soma for None por algum motivo, garantimos que seja 0.0
    if soma is None:
        soma = 0.0

    # Agora podemos arredondar sem problemas, já que soma é um número válido
    soma = round(soma, 2)
    disponivel = float(soma_rendimentos) - float(soma)

    # Formatação do número pra enviar a quantidade disponivel
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    disponivel_formatado = locale.format_string("%.2f", disponivel, grouping=True)

    if request.method == 'POST':
        form = SolicitarRetiradaForm(request.POST, request.FILES, user=request.user)

        if form.is_valid():
            valor = form.cleaned_data['valor']
            if valor > disponivel:
                messages.warning(request, f"ERRO AO TENTAR RETIRAR! R${disponivel} é o valor máximo!")
                return redirect('solicitar_retirada')
            else:
                # Salvando a retirada com aprovado=False e sem aprovador
                retirada = form.save(commit=False)
                retirada.cliente = cliente
                retirada.data_solicitacao = hoje
                retirada.aprovado = False  # Definindo aprovado como False
                retirada.aprovador = None  # Não atribuindo aprovador
                retirada.save()

            return redirect('retirada_investidor_list')  # Redireciona para a lista de retiradas do cliente
        else:
            # Se o formulário não for válido, exibe a mensagem de erro
            messages.error(request, "Senha incorreta ou erro nos dados fornecidos.")
    else:
        form = SolicitarRetiradaForm(user=request.user)

    return render(request, 'core/solicitar_retirada_form.html', {'form': form, 'cliente': cliente, 'disponivel':disponivel_formatado})

@login_required
def investimento_list(request):
    # Verificar se o usuário é um sócio
    socio = verificar_socio(request)
    if not socio:
        return redirect('index')
    investimentos = Investimento.objects.all().order_by('finalizado', '-data_inicio')

    # Defina a quantidade de itens por página
    itens_por_pagina = 100  # Ajuste conforme necessário

    paginator = Paginator(investimentos, itens_por_pagina)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Lógica para limitar o número de páginas exibidas
    num_paginas_visiveis = 3
    metade_num_paginas_visiveis = num_paginas_visiveis // 2
    numero_da_pagina = page_obj.number
    num_total_de_paginas = paginator.num_pages

    inicio_paginacao = max(1, numero_da_pagina - metade_num_paginas_visiveis)
    final_paginacao = min(num_total_de_paginas, inicio_paginacao + num_paginas_visiveis - 1)

    if final_paginacao - inicio_paginacao + 1 < num_paginas_visiveis:
        inicio_paginacao = max(1, final_paginacao - num_paginas_visiveis + 1)

    paginas_visiveis = range(inicio_paginacao, final_paginacao + 1)

    return render(request, 'core/investimento_list.html', {
        'investimentos': page_obj,
        'paginas_visiveis': paginas_visiveis,
    })

@login_required
def retirada_geral_list(request):
    socio = verificar_socio(request)  # A função verifica se é socio ou super, se nao for ele desloga e retorna False
    if not socio:
        return redirect('index')

    solicitacoes = Retirada.objects.filter(aprovado=False, finalizado=False)

    tem_solicitacoes = False
    if(len(solicitacoes) > 0):
        tem_solicitacoes = True

    retiradas = Retirada.objects.filter(aprovado=True, finalizado=False)

    return render(request, 'core/retirada_geral_list.html', {'tem_solicitacoes':tem_solicitacoes, 'retiradas':retiradas})

@login_required
def investidor_area_cartao_parcelas(request, pk):
    usuario = request.user
    cliente = Cliente.objects.get(usuario=usuario)
    tem_rendimentos = False
    try:
        investimento = Investimento.objects.get(pk=pk, cliente=cliente)
        if (investimento.rendimentos() != "0,00"):
            tem_rendimentos = True
    except Investimento.DoesNotExist:
        return HttpResponse("Investimento não encontrado.", status=404)

    return render(request, 'core/investidor_area_cartao_parcelas.html', {'investimento': investimento, 'tem_rendimentos':tem_rendimentos})


@login_required
def area_investidor_investimento_list(request):
    investidor = get_object_or_404(Cliente, usuario=request.user)
    investimentos = Investimento.objects.filter(cliente=investidor).order_by('finalizado', '-data_inicio')

    # Defina a quantidade de itens por página
    itens_por_pagina = 100  # Ajuste conforme necessário

    paginator = Paginator(investimentos, itens_por_pagina)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Lógica para limitar o número de páginas exibidas
    num_paginas_visiveis = 3
    metade_num_paginas_visiveis = num_paginas_visiveis // 2
    numero_da_pagina = page_obj.number
    num_total_de_paginas = paginator.num_pages

    inicio_paginacao = max(1, numero_da_pagina - metade_num_paginas_visiveis)
    final_paginacao = min(num_total_de_paginas, inicio_paginacao + num_paginas_visiveis - 1)

    if final_paginacao - inicio_paginacao + 1 < num_paginas_visiveis:
        inicio_paginacao = max(1, final_paginacao - num_paginas_visiveis + 1)

    paginas_visiveis = range(inicio_paginacao, final_paginacao + 1)

    return render(request, 'core/area_investidor_investimento_list.html', {
        'investidor': investidor,
        'investimentos': page_obj,
        'paginas_visiveis': paginas_visiveis,
    })

@login_required
def area_investidor_retirada_list(request):
    investidor = get_object_or_404(Cliente, usuario=request.user)
    retiradas = Retirada.objects.filter(cliente=investidor).order_by('-aprovado','-data_retirada')

    # Defina a quantidade de itens por página
    itens_por_pagina = 100  # Ajuste conforme necessário

    paginator = Paginator(retiradas, itens_por_pagina)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Lógica para limitar o número de páginas exibidas
    num_paginas_visiveis = 3
    metade_num_paginas_visiveis = num_paginas_visiveis // 2
    numero_da_pagina = page_obj.number
    num_total_de_paginas = paginator.num_pages

    inicio_paginacao = max(1, numero_da_pagina - metade_num_paginas_visiveis)
    final_paginacao = min(num_total_de_paginas, inicio_paginacao + num_paginas_visiveis - 1)

    if final_paginacao - inicio_paginacao + 1 < num_paginas_visiveis:
        inicio_paginacao = max(1, final_paginacao - num_paginas_visiveis + 1)

    paginas_visiveis = range(inicio_paginacao, final_paginacao + 1)

    return render(request, 'core/area_investidor_retirada_list.html', {
        'investidor': investidor,
        'retiradas': page_obj,
        'paginas_visiveis': paginas_visiveis,
    })

@login_required
def solicitacao_investimento_create(request):
    # Obtemos o cliente associado ao usuário logado
    cliente = Cliente.objects.get(usuario=request.user)
    periodo = Periodo.objects.filter(cliente=cliente, dinheiro=True, aberto=True).first()

    if request.method == 'POST':
        form = SolicitacaoInvestimentoForm(request.POST, request.FILES)
        if form.is_valid():
            senha = form.cleaned_data['senha']
            if not request.user.check_password(senha):
                messages.warning(request, "Senha incorreta.")
                return redirect('solicitacao_investimento_create')
            # Atribuímos o cliente logado ao campo cliente da solicitação
            solic_investimento = form.save(commit=False)
            solic_investimento.periodo = periodo
            solic_investimento.data_solicitacao = date.today()
            solic_investimento.save()
            messages.success(request, "Solicitação realizado com sucesso, aguarde a análise.")
            return redirect('investidor_area_investimentos')  # Redireciona para a lista de solicitações
    else:
        form = SolicitacaoInvestimentoForm()

    return render(request, 'core/solicitacao_investimento_create.html', {'form': form, 'cliente':cliente})

@login_required
def solicitacao_retirada_rendimento_create(request):
    # Obtemos o cliente associado ao usuário logado
    cliente = Cliente.objects.get(usuario=request.user)
    periodo = Periodo.objects.filter(cliente=cliente, dinheiro=True, aberto=True).first()
    solicitacao_anterior = Retirada.objects.filter(periodo=periodo,autorizado=False)
    if (len(solicitacao_anterior)>0):
        messages.success(request, "Solicitação existente.")
        return redirect('investidor_area_investimentos')  # Redireciona para a lista de solicitações
    disponivel = periodo.rendimento_disponivel_retirada()
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    disponivel_formatado = locale.format_string("%.2f", disponivel, grouping=True)

    if request.method == 'POST':
        form = SolicitacaoRetiradaRendimentoForm(request.POST, request.FILES)
        if form.is_valid():
            senha = form.cleaned_data['senha']
            if not request.user.check_password(senha):
                messages.warning(request, "Senha incorreta.")
                return redirect('solicitacao_retirada_rendimento_create')
            # Atribuímos o cliente logado ao campo cliente da solicitação
            valor = form.cleaned_data['valor']
            if(float(valor)>disponivel):
                messages.warning(request, "Valor não deve ultrapassar o disponível.")
                return redirect('solicitacao_retirada_rendimento_create')
            solic_retirada = form.save(commit=False)
            solic_retirada.periodo = periodo
            solic_retirada.data_solicitacao = date.today()
            solic_retirada.save()
            messages.success(request, "Solicitação realizado com sucesso, aguarde a análise.")
            return redirect('investidor_area_investimentos')  # Redireciona para a lista de solicitações
    else:
        form = SolicitacaoRetiradaRendimentoForm()

    return render(request, 'core/solicitacao_retirada_rendimento_create.html', {'form': form, 'disponivel_formatado':disponivel_formatado})

@login_required
def solicitacao_investimento_edit(request, pk):
    cliente = Cliente.objects.get(usuario=request.user)
    periodo = Periodo.objects.filter(cliente=cliente, dinheiro=True, aberto=True).first()
    solicitacao = Investimento.objects.get(pk=pk,periodo=periodo)

    if request.method == 'POST':
        form = SolicitacaoInvestimentoForm(request.POST, request.FILES, instance=solicitacao)

        if form.is_valid():
            senha = form.cleaned_data['senha']
            if not request.user.check_password(senha):
                messages.warning(request, "Senha incorreta.")
                return redirect('solicitacao_investimento_create')
            form.save()
            messages.success(request, "Solicitação atualizada com sucesso, aguarde a análise.")
            return redirect('investidor_area_investimentos')  # Redireciona para a lista de solicitações

    form = SolicitacaoInvestimentoForm(instance=solicitacao)
    return render(request, 'core/solicitacao_investimento_create.html', {'form': form})

@login_required
def solicitacao_retirada_rendimento_edit(request, pk):
    cliente = Cliente.objects.get(usuario=request.user)
    periodo = Periodo.objects.filter(cliente=cliente, dinheiro=True, aberto=True).first()
    solicitacao = Retirada.objects.get(pk=pk,periodo=periodo)

    disponivel = periodo.rendimento_disponivel_retirada()
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    disponivel_formatado = locale.format_string("%.2f", disponivel, grouping=True)

    if request.method == 'POST':
        form = SolicitacaoRetiradaRendimentoForm(request.POST, request.FILES, instance=solicitacao)

        if form.is_valid():
            senha = form.cleaned_data['senha']
            if not request.user.check_password(senha):
                messages.warning(request, "Senha incorreta.")
                return redirect('solicitacao_investimento_edit', pk)
            valor = form.cleaned_data['valor']
            if (float(valor) > disponivel):
                messages.warning(request, "Valor não deve ultrapassar o disponível.")
                return redirect('solicitacao_retirada_rendimento_edit', pk)
            form.save()
            messages.success(request, "Solicitação atualizada com sucesso, aguarde a análise.")
            return redirect('investidor_area_investimentos')  # Redireciona para a lista de solicitações

    form = SolicitacaoRetiradaRendimentoForm(instance=solicitacao)
    return render(request, 'core/solicitacao_retirada_rendimento_create.html', {'form': form,'disponivel_formatado':disponivel_formatado})

@login_required
def solicitacao_investimento_delete(request, pk):
    cliente = Cliente.objects.get(usuario=request.user)
    periodo = Periodo.objects.filter(cliente=cliente, dinheiro=True, aberto=True).first()
    solicitacao = Investimento.objects.get(pk=pk, periodo=periodo)

    # Se for um POST, verificar a senha do usuário
    if request.method == 'POST':
        senha = request.POST.get('senha')
        user = request.user

        # Verificar se a senha está correta
        if user.check_password(senha):
            solicitacao.delete()
            messages.success(request, "Solicitação excluída com sucesso.")
            return redirect('investidor_area_investimentos')
        else:
            # Se a senha estiver incorreta, exibe a mensagem de erro
            messages.error(request, "Senha incorreta. Tente novamente.")

    return render(request, 'core/solicitacao_investimento_delete.html', {'solicitacao': solicitacao})

@login_required
def solicitacao_retirada_rendimento_delete(request, pk):
    cliente = Cliente.objects.get(usuario=request.user)
    periodo = Periodo.objects.filter(cliente=cliente, dinheiro=True, aberto=True).first()
    solicitacao = Retirada.objects.get(pk=pk, periodo=periodo)

    # Se for um POST, verificar a senha do usuário
    if request.method == 'POST':
        senha = request.POST.get('senha')
        user = request.user

        # Verificar se a senha está correta
        if user.check_password(senha):
            solicitacao.delete()
            messages.success(request, "Solicitação excluída com sucesso.")
            return redirect('investidor_area_investimentos')
        else:
            # Se a senha estiver incorreta, exibe a mensagem de erro
            messages.error(request, "Senha incorreta. Tente novamente.")

    return render(request, 'core/solicitacao_retirada_rendimento_delete.html', {'solicitacao': solicitacao})


@login_required
def marcar_investimento_reinvestir(request, pk):
    # Verificar se o usuário é um sócio
    socio = verificar_socio(request)
    if not socio:
        return redirect('index')

    data = {}
    investimento = get_object_or_404(Investimento, pk=pk)
    if (investimento.autorizado == True and investimento.finalizado == False):
        investimento.marcado_reinvestir = True
        investimento.marcado_retirar = False
        investimento.save()

    return redirect('finalizar_periodo_novo', investimento.cliente.pk)

@login_required
def marcar_investimento_retirar(request, pk):
    # Verificar se o usuário é um sócio
    socio = verificar_socio(request)
    if not socio:
        return redirect('index')

    data = {}
    investimento = get_object_or_404(Investimento, pk=pk)
    if (investimento.autorizado == True and investimento.finalizado == False):
        investimento.marcado_reinvestir = False
        investimento.marcado_retirar = True
        investimento.save()

    return redirect('finalizar_periodo_novo', investimento.cliente.pk)

@login_required
def limpar_marcacao_investimento(request, pk):
    # Verificar se o usuário é um sócio
    socio = verificar_socio(request)
    if not socio:
        return redirect('index')

    data = {}
    investimento = get_object_or_404(Investimento, pk=pk)
    if (investimento.autorizado == True and investimento.finalizado == False):
        investimento.marcado_reinvestir = False
        investimento.marcado_retirar = False
        investimento.save()

    return redirect('finalizar_periodo_novo', investimento.cliente.pk)

@login_required
def marcar_rendimento_reinvestir(request, pk):
    # Verificar se o usuário é um sócio
    socio = verificar_socio(request)
    if not socio:
        return redirect('index')

    data = {}
    rendimento = get_object_or_404(Rendimento, pk=pk)
    if (rendimento.ativo):
        rendimento.marcado_reinvestir = True
        rendimento.marcado_retirar = False
        rendimento.save()

    return redirect('finalizar_periodo_novo', rendimento.investimento.cliente.pk)

@login_required
def marcar_rendimento_retirar(request, pk):
    # Verificar se o usuário é um sócio
    socio = verificar_socio(request)
    if not socio:
        return redirect('index')

    data = {}
    rendimento = get_object_or_404(Rendimento, pk=pk)
    if (rendimento.ativo):
        rendimento.marcado_reinvestir = False
        rendimento.marcado_retirar = True
        rendimento.save()

    return redirect('finalizar_periodo_novo', rendimento.investimento.cliente.pk)

@login_required
def limpar_marcacao_rendimento(request, pk):
    # Verificar se o usuário é um sócio
    socio = verificar_socio(request)
    if not socio:
        return redirect('index')

    data = {}
    rendimento = get_object_or_404(Rendimento, pk=pk)
    if (rendimento.ativo):
        rendimento.marcado_reinvestir = False
        rendimento.marcado_retirar = False
        rendimento.save()

    return redirect('finalizar_periodo_novo', rendimento.investimento.cliente.pk)

# autorizado = models.BooleanField(default=False)
# reinvestido = models.BooleanField(default=False)
# finalizado = models.BooleanField(default=False)
# retirado = models.BooleanField(default=False)

@login_required
def aprovar_solicitacao_aporte(request, pk):
    socio = verificar_socio(request)
    if not socio:
        return redirect('index')
    investimento = Investimento.objects.get(pk=pk)

    if request.method == 'POST':
        form = AprovarInvestimentoDinheiroForm(request.POST, instance=investimento, user=request.user)
        if form.is_valid():
            investimento = form.save(commit=False)
            valor = investimento.valor
            porcent_rend_valor = investimento.porcent_rend_valor

            # Calcular rendimentos
            if porcent_rend_valor is not None and valor is not None:
                rendimentos = round((float(valor) * float(porcent_rend_valor)) / 100, 2)
                investimento.valor_rendimento = rendimentos
            else:
                investimento.valor_rendimento = 0

            investimento.autorizado = True
            investimento.autorizador = request.user
            investimento.reinvestido = False
            investimento.save()
            messages.success(request, "Aporte aprovado com sucesso.")

            return redirect('periodo_dinheiro_list', investimento.periodo.pk)  # Redireciona para a lista de investimentos do cliente
        else:
            # Se o formulário não for válido, exibe a mensagem de erro
            messages.error(request, "Senha incorreta ou erro nos dados fornecidos.")
    else:
        form = AprovarInvestimentoDinheiroForm(user=request.user)
    return render(request, 'core/aprovar_solicitacao_aporte.html', {'investimento': investimento, 'periodo':periodo, 'form':form})

@login_required
def aprovar_solicitacao_rendimento(request, pk):
    socio = verificar_socio(request)
    if not socio:
        return redirect('index')
    retirada = Retirada.objects.get(pk=pk)

    if request.method == 'POST':
        form = AprovarRetiradaRendimentoForm(request.POST, instance=retirada, user=request.user)
        if form.is_valid():
            retirada = form.save(commit=False)
            retirada.autorizado = True
            retirada.autorizador = request.user
            retirada.save()
            messages.success(request, "Solicitação de rendimento aprovada com sucesso.")

            return redirect('periodo_dinheiro_list', retirada.periodo.pk)  # Redireciona para a lista de investimentos do cliente
        else:
            # Se o formulário não for válido, exibe a mensagem de erro
            messages.error(request, "Erro no formulário.")
    else:
        form = AprovarRetiradaRendimentoForm(user=request.user)
    return render(request, 'core/aprovar_solicitacao_rendimento.html', {'retirada': retirada, 'periodo':periodo, 'form':form})

@login_required
def finalizar_periodo_novo(request, pk):
    # Verificar se o usuário é um sócio
    socio = verificar_socio(request)
    if not socio:
        return redirect('index')

    periodo = get_object_or_404(Periodo, pk=pk)
    cliente = periodo.cliente
    valor_disponivel = float(periodo.disponivel_retirada_total())
    if not periodo.aberto:
        messages.warning(request, "Este período está fechado.")
        return redirect('periodo_dinheiro_list', periodo.pk)

    # Caso o método seja POST, tentamos processar o formulário
    if request.method == 'POST':
        form = FinalizarPeriodoForm(request.POST, user=request.user)
        if form.is_valid():

            senha = form.cleaned_data['senha_administrador']
            if not request.user.check_password(senha):
                messages.warning(request, "Senha incorreta.")
                return redirect('finalizar_periodo_novo', periodo.pk)

            periodo.aberto = False
            periodo.save()
            periodo_novo = Periodo.objects.create(
                cliente=cliente,
                dinheiro=True,
                data_inicio = form.cleaned_data['data_inicio'],
                data_fim = form.cleaned_data['data_fim'],
                alavancagem=False,
                aberto=True
            )

            if (valor_disponivel > 0):
                porcent_rend_valor = form.cleaned_data['porcentagem_rendimentos']
                # Calcular rendimentos
                rendimentos = 0
                if porcent_rend_valor is not None:
                    rendimentos = round((float(valor_disponivel) * float(porcent_rend_valor)) / 100, 2)
                reinvestimento = Investimento.objects.create(
                    periodo=periodo_novo,
                    socio=form.cleaned_data['socio'],
                    data_inicio=form.cleaned_data['data_inicio'],
                    data_fim=form.cleaned_data['data_fim'],
                    valor = float(valor_disponivel),
                    valor_rendimento = rendimentos,
                    porcent_rend_valor = float(porcent_rend_valor),
                    autorizador = request.user,
                    autorizado = True,
                    reinvestido = True
                )

            if (periodo.soma_retiradas_float()>0):
                Retirada.objects.create(
                    periodo=periodo,
                    data = form.cleaned_data['data_fim'],
                    valor = periodo.soma_retiradas_float(),
                    autorizado = True,
                    autorizador = request.user
                )
            messages.success(request, "Período finalizado com sucesso.")
            return redirect('periodo_dinheiro_list', periodo_novo.pk)
        else:
            print(form.errors)  # Exibe os erros do formulário
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Erro no campo '{form.fields[field].label}': {error}")
            messages.error(request, "Há erros no formulário. Por favor, corrija-os.")

    # Se o método for GET ou o formulário for inválido, mostramos o formulário
    else:
        form = FinalizarPeriodoForm(user=request.user)

    return render(request, 'core/finalizar_periodo_novo.html', {'form': form, 'periodo': periodo, 'sera_investido': valor_disponivel, 'sera_retirado':periodo.soma_retiradas()})

@login_required
def investimento_cartao_finalizar(request, pk):
    # Verificar se o usuário é um sócio
    socio = verificar_socio(request)
    if not socio:
        return redirect('index')

    investimento_cartao = get_object_or_404(InvestimentoCartao, pk=pk)
    periodo = Periodo.objects.filter(cliente=investimento_cartao.cliente, dinheiro=True, aberto=True).first()

    # Caso o método seja POST, tentamos processar o formulário
    if request.method == 'POST':
        form = InvestimentoCartaoFinalizarForm(request.POST, user=request.user)
        if form.is_valid():

            senha = form.cleaned_data['senha_administrador']
            if not request.user.check_password(senha):
                messages.warning(request, "Senha incorreta.")
                return redirect('finalizar_periodo_novo', investimento_cartao.pk)

            investimento_cartao.aberto = False
            investimento_cartao.save()
            messages.success(request, "Investimento de cartão finalizado com sucesso.")
            return redirect('periodo_dinheiro_list', periodo.pk)

    else:
        form = InvestimentoCartaoFinalizarForm(user=request.user)

    return render(request, 'core/investimento_cartao_finalizar_form.html', {'form': form, 'investimento_cartao': investimento_cartao})

@login_required
def investimentos_anteriores_dinheiro(request, pk):
    socio = verificar_socio(request)  # A função verifica se é socio, se nao for ele desloga e retorna False
    if not socio:
        return redirect('index')
    cliente = get_object_or_404(Cliente, pk=pk)
    investimentos_anteriores_dinheiro = Investimento.objects.filter(periodo__cliente=cliente, periodo__aberto=False, autorizado=True, periodo__dinheiro=True).order_by('-data_inicio')
    return render(request, 'core/investimentos_anteriores_dinheiro.html', {'cliente': cliente,'investimentos_anteriores_dinheiro': investimentos_anteriores_dinheiro})

@login_required
def investimentos_anteriores_cartao(request, pk):
    socio = verificar_socio(request)  # A função verifica se é socio, se nao for ele desloga e retorna False
    if not socio:
        return redirect('index')
    cliente = get_object_or_404(Cliente, pk=pk)
    investimentos_anteriores_cartao = InvestimentoCartao.objects.filter(cliente=cliente, aberto=False, autorizado=True).order_by('-data_inicio')
    return render(request, 'core/investimentos_anteriores_cartao.html', {'cliente': cliente,'investimentos_anteriores_cartao': investimentos_anteriores_cartao})

@login_required
def contrato(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    return render(request, 'core/contrato.html', {'investidor':cliente})