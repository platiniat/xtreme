from django.db import models
from django.utils import timezone
from django.db.models import Sum, F
from datetime import timedelta, datetime
from django.contrib.auth.models import User
import locale

class Superusuario(models.Model):
    usuario = models.OneToOneField(User, blank=True, null=True, on_delete=models.PROTECT)
    nome = models.CharField(max_length=255)

# Modelo Conta
class Agencia(models.Model):
    nome = models.CharField(max_length=255)
    data_criacao = models.DateField(verbose_name='Data da criação', blank=True, null=True)
    cnpj = models.CharField(verbose_name='CNPJ',max_length=30, blank=True, null=True)
    endereco = models.TextField(verbose_name='Endereço',blank=True, null=True)
    gerente = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nome

    def numero(self):
        return "00"+str(self.pk)

    def chaves_pix(self):
        return list(Pix_agencia.objects.filter(agencia=self))

class Pix_agencia(models.Model):
    agencia = models.ForeignKey(Agencia, on_delete=models.PROTECT)
    nome = models.CharField(max_length=255)
    banco = models.CharField(max_length=255)
    chave = models.CharField(max_length=255)
    cpf_cnpj = models.CharField(verbose_name='CPF/CNPJ', max_length=30, blank=True, null=True)

    def __str__(self):
        return self.chave

# Modelo Conta
class Socio(models.Model):
    usuario = models.OneToOneField(User, blank=True, null=True, on_delete=models.PROTECT)
    nome = models.CharField(max_length=255)
    data_inicio = models.DateField(verbose_name="Data de início", blank=True, null=True)
    telefone = models.CharField(max_length=20)
    cpf = models.CharField(max_length=14, unique=True)
    foto = models.ImageField(upload_to='fotos/', blank=True, null=True)
    endereco = models.TextField(verbose_name='Endereço', blank=True, null=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

    def codigo(self):
        return "00"+str(self.pk)

# Modelo Cliente
class Cliente(models.Model):
    usuario = models.OneToOneField(User, blank=True, null=True, on_delete=models.PROTECT)
    data = models.DateField(verbose_name="Data do cadastro", blank=True, null=True)
    nome = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20)
    cpf = models.CharField(max_length=14, unique=True)
    data_nascimento = models.DateField(verbose_name='Data de Nascimento', blank=True, null=True)
    endereco = models.TextField()
    conjuge_segurado = models.CharField(verbose_name="Nome do Cônjuge/Segurado", blank=True, null=True, max_length=255)
    cpf_conjuge = models.CharField(verbose_name="CPF do Cônjuge/Segurado",max_length=14, blank=True, null=True)
    data_nascimento_conjuge = models.DateField(verbose_name='Data de Nascimento do Cônjuge/Segurado', blank=True, null=True)
    telefone_conjuge = models.CharField(verbose_name='Telefone do Cônjuge/Segurado',max_length=20, blank=True, null=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


# Modelo Conta
class Conta(models.Model):
    agencia = models.ForeignKey(Agencia, on_delete=models.PROTECT, blank=True, null=True)
    data_abertura = models.DateField()
    porcentagem = models.DecimalField(max_digits=10, decimal_places=2, default=10)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    socio = models.ForeignKey(Socio, on_delete=models.PROTECT, blank=True, null=True)
    def __str__(self):
        return str(self.numero())

    def numero(self):
        return "0000"+str(self.pk)


class Periodo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    data_inicio = models.DateField(blank=True, null=True)
    data_fim = models.DateField(verbose_name="Data de fechamento", blank=True, null=True)
    dinheiro = models.BooleanField(default=True)
    alavancagem = models.BooleanField(default=False)
    aberto = models.BooleanField(default=False)

    def __str__(self):
        return str(self.cliente.nome)

    def solicitacoes_investimentos(self):
        return list(Investimento.objects.filter(periodo=self, autorizado=False))

    def soma_solicitacoes_investimentos(self):
        investimentos = Investimento.objects.filter(
            periodo=self,
            autorizado=False
        ).aggregate(Sum('valor'))['valor__sum'] or 0
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        return locale.format_string("%.2f", investimentos, grouping=True)

    def investimentos(self):
        return list(Investimento.objects.filter(periodo=self, autorizado=True))

    def soma_investimentos(self):
        investimentos = Investimento.objects.filter(
            periodo=self,
            autorizado=True
        ).aggregate(Sum('valor'))['valor__sum'] or 0
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        return locale.format_string("%.2f", investimentos, grouping=True)

    def soma_rendimentos(self):
        rendimentos = Investimento.objects.filter(
            periodo=self,
            autorizado=True
        ).aggregate(Sum('valor_rendimento'))['valor_rendimento__sum'] or 0
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        return locale.format_string("%.2f", rendimentos, grouping=True)

    def solicitacoes_retiradas(self):
        return list(Retirada.objects.filter(periodo=self, autorizado=False))

    def soma_solicitacoes_retiradas(self):
        retiradas = Retirada.objects.filter(
            periodo=self,
            autorizado=False
        ).aggregate(Sum('valor'))['valor__sum'] or 0
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        return locale.format_string("%.2f", retiradas, grouping=True)

    def retiradas(self):
        return list(Retirada.objects.filter(periodo=self, autorizado=True))

    def soma_retiradas_float(self):
        retiradas = Retirada.objects.filter(
            periodo=self,
            autorizado=True
        ).aggregate(Sum('valor'))['valor__sum'] or 0
        return round(float(retiradas),2)

    def soma_retiradas(self):
        retiradas = Retirada.objects.filter(
            periodo=self,
            autorizado=True
        ).aggregate(Sum('valor'))['valor__sum'] or 0
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        return locale.format_string("%.2f", retiradas, grouping=True)

    def disponivel_retirada_total(self):
        # Calculando o valor total de investimentos autorizados
        rendimento_cartao = InvestimentoCartao.objects.filter(
            aberto=True,
            cliente=self.cliente
        ).aggregate(rendimento_mes=Sum('rendimento_mes'))['rendimento_mes'] or 0

        investimentos = Investimento.objects.filter(
            periodo=self,
            autorizado=True
        ).aggregate(Sum('valor'))[
                            'valor__sum'] or 0  # Certifique-se de acessar o valor correto no dicionário de agregação

        # Calculando o valor total de rendimentos autorizados
        rendimentos = Investimento.objects.filter(
            periodo=self,
            autorizado=True
        ).aggregate(Sum('valor_rendimento'))['valor_rendimento__sum'] or 0  # Acessando o campo corretamente

        # Somando investimentos e rendimentos
        positivo = float(investimentos) + float(rendimentos) + float(rendimento_cartao)

        # Calculando o total de retiradas autorizadas
        retiradas = Retirada.objects.filter(
            periodo=self,
            autorizado=True
        ).aggregate(Sum('valor'))['valor__sum'] or 0  # Acessando o valor correto no dicionário de agregação

        # Calculando o saldo disponível para retirada
        saldo = round(float(positivo) - float(retiradas), 2)
        return float(saldo)

    def reinvestir_formatado(self):
        # Calculando o valor total de investimentos autorizados
        rendimento_cartao = InvestimentoCartao.objects.filter(
            aberto=True,
            cliente=self.cliente
        ).aggregate(rendimento_mes=Sum('rendimento_mes'))['rendimento_mes'] or 0

        investimentos = Investimento.objects.filter(
            periodo=self,
            autorizado=True
        ).aggregate(Sum('valor'))[
                            'valor__sum'] or 0  # Certifique-se de acessar o valor correto no dicionário de agregação

        # Calculando o valor total de rendimentos autorizados
        rendimentos = Investimento.objects.filter(
            periodo=self,
            autorizado=True
        ).aggregate(Sum('valor_rendimento'))['valor_rendimento__sum'] or 0  # Acessando o campo corretamente

        # Somando investimentos e rendimentos
        positivo = float(investimentos) + float(rendimentos) + float(rendimento_cartao)

        # Calculando o total de retiradas autorizadas
        retiradas = Retirada.objects.filter(
            periodo=self,
            autorizado=True
        ).aggregate(Sum('valor'))['valor__sum'] or 0  # Acessando o valor correto no dicionário de agregação

        # Calculando o saldo disponível para retirada
        saldo = round(float(positivo) - float(retiradas), 2)
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        return locale.format_string("%.2f", saldo, grouping=True)


    def rendimento_disponivel_retirada(self):
        rendimentos = Investimento.objects.filter(
            periodo=self,
            autorizado=True
        ).aggregate(rendimento=Sum('valor_rendimento'))['rendimento'] or 0

        rendimento_cartao = InvestimentoCartao.objects.filter(
            aberto=True,
            cliente=self.cliente
        ).aggregate(rendimento_total=Sum('rendimento_mes'))['rendimento_total'] or 0

        retiradas = Retirada.objects.filter(
            periodo=self,
            autorizado=True
        ).aggregate(retiradas=Sum('valor'))['retiradas'] or 0

        saldo = round(float(rendimentos) + float(rendimento_cartao) - float(retiradas),2)
        return float(saldo)

    def investimentos_cartoes_abertos(self):
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        data={}
        data['investimentos_cartoes'] = InvestimentoCartao.objects.filter(
            aberto=True,
            cliente=self.cliente
        ).order_by('data_fim')
        investido = InvestimentoCartao.objects.filter(
            aberto=True,
            cliente=self.cliente
        ).aggregate(investido=Sum('valor_real'))['investido'] or 0
        data['investido'] = locale.format_string("%.2f", investido, grouping=True)

        maquineta = InvestimentoCartao.objects.filter(
            aberto=True,
            cliente=self.cliente
        ).aggregate(maquineta=Sum('valor_maquineta'))['maquineta'] or 0
        data['maquineta'] = locale.format_string("%.2f", maquineta, grouping=True)

        rendimento_total = InvestimentoCartao.objects.filter(
            aberto=True,
            cliente=self.cliente
        ).aggregate(rendimento_total=Sum('rendimento_total'))['rendimento_total'] or 0
        data['rendimento_total'] = locale.format_string("%.2f", rendimento_total, grouping=True)

        rendimento_mes = InvestimentoCartao.objects.filter(
            aberto=True,
            cliente=self.cliente
        ).aggregate(rendimento_mes=Sum('rendimento_mes'))['rendimento_mes'] or 0
        data['rendimento_mes'] = locale.format_string("%.2f", rendimento_mes, grouping=True)
        data['num_cartoes_abertos'] = len(InvestimentoCartao.objects.filter(aberto=True, cliente=self.cliente))

        # Filtrar os investimentos de cartões abertos que têm data_inicio e data_fim no mês e ano atuais
        hoje = datetime.today()
        mes_ano_atual = hoje.strftime('%Y-%m')  # Formato 'YYYY-MM'

        investimentos_mes_ano_atual = data['investimentos_cartoes'].filter(
            data_inicio__year=hoje.year,
            data_inicio__month=hoje.month,
            data_fim__year=hoje.year,
            data_fim__month=hoje.month
        )

        # Soma dos valores dos investimentos que atendem à condição do mês e ano atual
        investido_mes_atual = investimentos_mes_ano_atual.aggregate(investido_mes_atual=Sum('valor_real'))['investido_mes_atual'] or 0
        data['investido_mes_atual'] = locale.format_string("%.2f", investido_mes_atual, grouping=True)

        return data


class Investimento(models.Model):
    periodo = models.ForeignKey(Periodo, on_delete=models.PROTECT,blank=True, null=True)
    socio = models.ForeignKey(Socio, on_delete=models.PROTECT, blank=True, null=True)
    data_inicio = models.DateField(blank=True, null=True)
    data_fim = models.DateField(verbose_name="Data de fechamento", blank=True, null=True)
    valor = models.DecimalField(verbose_name="Valor", max_digits=20, decimal_places=2)
    valor_rendimento = models.DecimalField(verbose_name="Valor Rendimento", max_digits=20, decimal_places=2, default=0)
    porcent_rend_valor = models.DecimalField(verbose_name="% rendimento", max_digits=20, decimal_places=2, blank=True, null=True)
    comprovante = models.FileField(upload_to='comprovantes-investimentos/', null=True, blank=True)
    autorizador = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT, related_name="autorizador")
    autorizado = models.BooleanField(default=False)
    data_solicitacao = models.DateField(blank=True, null=True)
    reinvestido = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    def modo(self):
        if self.dinheiro:
            return {"tipo":"DINHEIRO", "cor":"green","icone":"fa fa-money"}
        elif self.alavancagem:
            return {"tipo":"ALAVANCAGEM", "cor":"#4e61a5","icone":"fa fa-rocket"}


    def valor_formatado(self):
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        numero = self.valor
        # Formatação do número
        return locale.format_string("%.2f", numero, grouping=True)

    def valor_rendimento_formatado(self):
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        numero = self.valor_rendimento
        # Formatação do número
        return locale.format_string("%.2f", numero, grouping=True)


class Retirada(models.Model):
    periodo = models.ForeignKey(Periodo, on_delete=models.PROTECT,blank=True, null=True)
    data_solicitacao = models.DateField(blank=True, null=True)
    data = models.DateField(blank=True, null=True)
    valor = models.DecimalField(max_digits=20, decimal_places=2)
    chave_pix = models.CharField(verbose_name="Chave pix", max_length=255, blank=True, null=True)
    banco_pix = models.CharField(verbose_name="Banco", max_length=255, blank=True, null=True)
    titular_pix = models.CharField(verbose_name="Titular", max_length=255, blank=True, null=True)
    comprovante = models.FileField(upload_to='comprovantes-prestacao/', null=True, blank=True)
    autorizado = models.BooleanField(default=False)
    autorizador = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)

    def data_formatada(self):
        return self.data_retirada.strftime('%d/%m/%Y')

    def valor_formatado(self):
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        numero = self.valor
        # Formatação do número
        return locale.format_string("%.2f", numero, grouping=True)

class InvestimentoCartao(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    socio = models.ForeignKey(Socio, on_delete=models.PROTECT, blank=True, null=True)
    data_inicio = models.DateField(verbose_name="Data inicio",blank=True, null=True)
    data_fim = models.DateField(verbose_name="Data fim", blank=True, null=True)
    valor_maquineta = models.DecimalField(verbose_name="Valor maquineta", max_digits=30, decimal_places=2)
    num_prestacoes = models.PositiveIntegerField(default=0)
    valor_prestacao = models.DecimalField(verbose_name="Valor prestação", max_digits=30, decimal_places=2,default=0)
    valor_real = models.DecimalField(verbose_name="Valor Investido", max_digits=30, decimal_places=2)
    rendimento_total = models.DecimalField(verbose_name="Valor Rendimento total", max_digits=30, decimal_places=2, default=0)
    rendimento_mes = models.DecimalField(verbose_name="Valor Rendimento mês", max_digits=30, decimal_places=2, default=0)
    porcent_rend_valor = models.DecimalField(verbose_name="% rendimento", max_digits=30, decimal_places=2, blank=True, null=True)
    comprovante = models.FileField(upload_to='comprovantes-investimentos/', null=True, blank=True)
    autorizador = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)
    autorizado = models.BooleanField(default=True)
    aberto = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)

    def parcelas(self):
        return PrestacaoCartao.objects.filter(investimento_cartao=self).order_by('-data')

    def valor_maquineta_formatado(self):
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        numero = self.valor_maquineta
        # Formatação do número
        return locale.format_string("%.2f", numero, grouping=True)

    def valor_prestacao_formatado(self):
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        numero = self.valor_prestacao
        # Formatação do número
        return locale.format_string("%.2f", numero, grouping=True)

    def valor_real_formatado(self):
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        numero = self.valor_real
        # Formatação do número
        return locale.format_string("%.2f", numero, grouping=True)

    def rendimento_total_formatado(self):
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        numero = self.rendimento_total
        # Formatação do número
        return locale.format_string("%.2f", numero, grouping=True)

    def rendimento_mes_formatado(self):
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        numero = self.rendimento_mes
        # Formatação do número
        return locale.format_string("%.2f", numero, grouping=True)

class PrestacaoCartao(models.Model):
    investimento_cartao = models.ForeignKey(InvestimentoCartao, on_delete=models.PROTECT)
    data = models.DateField(verbose_name="Data vencimento")
    data_pagamento = models.DateField(verbose_name="Data pagamento", blank=True, null=True)
    valor = models.DecimalField(verbose_name="Valor", max_digits=30, decimal_places=2)
    autorizador = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT, related_name="autorizador_prestacao")
    autorizado = models.BooleanField(default=False)
    confirmador_pagamento = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT,related_name="confirmador_pagamento_prestacao")
    cancelador_pagamento = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT, related_name="cancelador_pagamento_prestacao")
    pago = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    def valor_formatado(self):
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        numero = self.valor
        # Formatação do número
        return locale.format_string("%.2f", numero, grouping=True)