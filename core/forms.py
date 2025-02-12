from decimal import Decimal

from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError

from .models import *

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['data','nome', 'telefone', 'cpf', 'data_nascimento', 'endereco', 'conjuge_segurado','cpf_conjuge','data_nascimento_conjuge','telefone_conjuge', 'ativo']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'conjuge_segurado': forms.TextInput(attrs={'class': 'form-control'}),
            'data_nascimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_nascimento_conjuge': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'endereco': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'id': 'cpf', 'class': 'form-control'}),
            'cpf_conjuge': forms.TextInput(attrs={'id': 'cpf_conjuge', 'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'id': 'telefone', 'class': 'form-control'}),
            'telefone_conjuge': forms.TextInput(attrs={'id': 'telefone_conjuge', 'class': 'form-control'}),
        }

        def __init__(self, *args, **kwargs):
            super(ClienteForm, self).__init__(*args, **kwargs)
            for field in self.fields.values():
                field.widget.attrs.update({'class': 'form-control'})

class AgenciaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AgenciaForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Agencia
        fields = ['nome', 'data_criacao', 'cnpj','gerente','endereco']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'data_criacao': forms.DateInput(attrs={'type': 'date'}),
        }

class PixAgenciaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PixAgenciaForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
    class Meta:
        model = Pix_agencia
        fields = ['nome', 'banco', 'chave', 'cpf_cnpj']  # Campos necessários para a chave PIX


class SocioForm(forms.ModelForm):

    class Meta:
        model = Socio
        fields = ['nome','data_inicio', 'cpf', 'telefone', 'foto', 'endereco', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'id': 'cpf', 'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'id': 'telefone', 'class': 'form-control'}),
            'data_inicio': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
            'endereco': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class ContaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContaForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Conta
        fields = ['agencia','data_abertura', 'porcentagem','socio']
        widgets = {
            'data_abertura': forms.DateInput(attrs={'type': 'date'}),
            'porcentagem': forms.TextInput(attrs={'value': 10}),
        }



class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Senha atual',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    new_password1 = forms.CharField(
        label='Nova senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    new_password2 = forms.CharField(
        label='Confirmação de nova senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )


class InvestimentoDinheiroForm(forms.ModelForm):
    class Meta:
        model = Investimento
        fields = ['data_inicio', 'data_fim', 'valor', 'porcent_rend_valor', 'socio']
        widgets = {
            'valor': forms.TextInput(attrs={'id': 'valor', 'class': 'form-control'}),
        }

    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Senha',
        required=True,
        help_text="Digite sua senha para confirmar a operação."
    )

    def __init__(self, *args, **kwargs):
        # Adicionando o usuário autenticado ao formulário
        self.user = kwargs.pop('user', None)
        super(InvestimentoDinheiroForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get('data_inicio')
        data_fim = cleaned_data.get('data_fim')

        # Validar se a data_fim não é antes de data_inicio
        if data_inicio and data_fim and data_fim < data_inicio:
            raise ValidationError("A data final não pode ser menor que data de início.")

        senha = cleaned_data.get('senha')
        if senha:
            # Verificar se o usuário está autenticado e se a senha fornecida está correta
            if not self.user.check_password(senha):
                raise ValidationError("Senha incorreta. Tente novamente.")

        return cleaned_data

    data_inicio = forms.DateField(
        label='Data de inicio',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'  # Para um seletor de data
        })
    )

    data_fim = forms.DateField(
        label='Data final',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'  # Para um seletor de data
        })
    )

class InvestimentoAlavancagemForm(forms.ModelForm):
    class Meta:
        model = Investimento
        fields = ['data_inicio', 'data_fim', 'valor', 'porcent_rend_valor', 'socio']
        widgets = {
            'valor': forms.TextInput(attrs={'id': 'valor', 'class': 'form-control'}),
        }

    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Senha',
        required=True,
        help_text="Digite sua senha para confirmar a operação."
    )

    def __init__(self, *args, **kwargs):
        # Adicionando o usuário autenticado ao formulário
        self.user = kwargs.pop('user', None)
        super(InvestimentoAlavancagemForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get('data_inicio')
        data_fim = cleaned_data.get('data_fim')

        # Validar se a data_fim não é antes de data_inicio
        if data_inicio and data_fim and data_fim < data_inicio:
            raise ValidationError("A data final não pode ser menor que data de início.")

        senha = cleaned_data.get('senha')
        if senha:
            # Verificar se o usuário está autenticado e se a senha fornecida está correta
            if not self.user.check_password(senha):
                raise ValidationError("Senha incorreta. Tente novamente.")

        return cleaned_data

    data_inicio = forms.DateField(
        label='Data de inicio',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'  # Para um seletor de data
        })
    )

    data_fim = forms.DateField(
        label='Data final',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'  # Para um seletor de data
        })
    )

class AprovarInvestimentoDinheiroForm(forms.ModelForm):
    class Meta:
        model = Investimento
        fields = ['data_inicio', 'data_fim', 'porcent_rend_valor', 'socio']

    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Senha',
        required=True,
        help_text="Digite sua senha para confirmar a operação."
    )

    def __init__(self, *args, **kwargs):
        # Adicionando o usuário autenticado ao formulário
        self.user = kwargs.pop('user', None)
        super(AprovarInvestimentoDinheiroForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get('data_inicio')
        data_fim = cleaned_data.get('data_fim')

        # Validar se a data_fim não é antes de data_inicio
        if data_inicio and data_fim and data_fim < data_inicio:
            raise ValidationError("A data final não pode ser menor que data de início.")

        senha = cleaned_data.get('senha')
        if senha:
            # Verificar se o usuário está autenticado e se a senha fornecida está correta
            if not self.user.check_password(senha):
                raise ValidationError("Senha incorreta. Tente novamente.")

        return cleaned_data

    data_inicio = forms.DateField(
        label='Data de inicio',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'  # Para um seletor de data
        })
    )

    data_fim = forms.DateField(
        label='Data final',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'  # Para um seletor de data
        })
    )

class AprovarRetiradaRendimentoForm(forms.ModelForm):
    class Meta:
        model = Retirada
        fields = ['data']

    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Senha',
        required=True,
        help_text="Digite sua senha para confirmar a operação."
    )

    def __init__(self, *args, **kwargs):
        # Adicionando o usuário autenticado ao formulário
        self.user = kwargs.pop('user', None)
        super(AprovarRetiradaRendimentoForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get('senha')
        if senha:
            # Verificar se o usuário está autenticado e se a senha fornecida está correta
            if not self.user.check_password(senha):
                raise ValidationError("Senha incorreta. Tente novamente.")
        return cleaned_data

    data = forms.DateField(
        label='Data',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'  # Para um seletor de data
        })
    )

class InvestimentoAlavancagemForm(forms.ModelForm):
    class Meta:
        model = Investimento
        fields = ['data_inicio', 'data_fim', 'valor', 'porcent_rend_valor','socio']
        widgets = {
            'valor': forms.TextInput(attrs={'id': 'valor', 'class': 'form-control'}),
        }

    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Senha',
        required=True,
        help_text="Digite sua senha para confirmar a operação."
    )

    def __init__(self, *args, **kwargs):
        # Adicionando o usuário autenticado ao formulário
        self.user = kwargs.pop('user', None)
        super(InvestimentoAlavancagemForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get('data_inicio')
        data_fim = cleaned_data.get('data_fim')

        # Validar se a data_fim não é antes de data_inicio
        if data_inicio and data_fim and data_fim < data_inicio:
            raise ValidationError("A data final não pode ser menor que data de início.")

        senha = cleaned_data.get('senha')
        if senha:
            # Verificar se o usuário está autenticado e se a senha fornecida está correta
            if not self.user.check_password(senha):
                raise ValidationError("Senha incorreta. Tente novamente.")

        return cleaned_data

    data_inicio = forms.DateField(
        label='Data de inicio',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'  # Para um seletor de data
        })
    )

    data_fim = forms.DateField(
        label='Data final',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'  # Para um seletor de data
        })
    )

class RetiradaForm(forms.ModelForm):
    class Meta:
        model = Retirada
        fields = ['data', 'valor', 'comprovante', 'chave_pix', 'banco_pix','titular_pix']
        widgets = {
            'valor': forms.TextInput(attrs={'id': 'valor', 'class': 'form-control'}),
        }

    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Senha',
        required=True,
        help_text="Digite sua senha para confirmar a operação."
    )

    def __init__(self, *args, **kwargs):
        # Adicionando o usuário autenticado ao formulário
        self.user = kwargs.pop('user', None)
        super(RetiradaForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get('data_retirada')

        senha = cleaned_data.get('senha')
        if senha:
            # Verificar se o usuário está autenticado e se a senha fornecida está correta
            if not self.user.check_password(senha):
                raise ValidationError("Senha incorreta. Tente novamente.")

        return cleaned_data

    data = forms.DateField(
        label='Data',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'  # Para um seletor de data
        })
    )


class FinalizarPeriodoForm(forms.Form):
    data_inicio = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Data Início")
    data_fim = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Data Fim")
    porcentagem_rendimentos = forms.DecimalField(max_digits=5, decimal_places=2, label="Porcentagem Rendimentos")
    senha_administrador = forms.CharField(widget=forms.PasswordInput(), label="Senha Administrador")
    socio = forms.ModelChoiceField(queryset=Socio.objects.all(), label="Sócio", required=True)

    def __init__(self, *args, **kwargs):
        # Adicionando o usuário autenticado ao formulário
        self.user = kwargs.pop('user', None)
        super(FinalizarPeriodoForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get("data_inicio")
        data_fim = cleaned_data.get("data_fim")

        # Valida se a data início é anterior à data fim
        if data_inicio and data_fim:
            if data_inicio >= data_fim:
                raise ValidationError("A Data Início deve ser anterior à Data Fim.")

        return cleaned_data

class SolicitarRetiradaForm(forms.ModelForm):
    class Meta:
        model = Retirada
        fields = ['valor', 'chave_pix', 'banco_pix','titular_pix']
        widgets = {
            'valor': forms.TextInput(attrs={'id': 'valor', 'class': 'form-control'}),
        }

    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Senha',
        required=True,
        help_text="Digite sua senha para confirmar a operação."
    )

    def __init__(self, *args, **kwargs):
        # Adicionando o usuário autenticado ao formulário
        self.user = kwargs.pop('user', None)
        super(SolicitarRetiradaForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()

        senha = cleaned_data.get('senha')
        if senha:
            # Verificar se o usuário está autenticado e se a senha fornecida está correta
            if not self.user.check_password(senha):
                raise ValidationError("Senha incorreta. Tente novamente.")

        return cleaned_data

class PeriodoForm(forms.ModelForm):
    class Meta:
        model = Periodo
        fields = ['data_inicio', 'data_fim']  # Inclua os campos necessários

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizando o widget para o campo 'data_inicio' e 'data_fim' para uma apresentação melhor
        self.fields['data_inicio'].widget = forms.DateInput(attrs={'type': 'date','class':'form-control'})
        self.fields['data_fim'].widget = forms.DateInput(attrs={'type': 'date','class':'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        # Lógica adicional de validação, caso necessário
        data_inicio = cleaned_data.get('data_inicio')
        data_fim = cleaned_data.get('data_fim')

        if data_inicio and data_fim:
            if data_fim < data_inicio:
                raise forms.ValidationError("A data de fim não pode ser anterior à data de início.")

        return cleaned_data


class InvestimentoCartaoForm(forms.ModelForm):

    class Meta:
        model = InvestimentoCartao
        fields = ['socio', 'data_inicio', 'data_fim', 'valor_maquineta', 'num_prestacoes', 'valor_real',
                  'porcent_rend_valor', 'comprovante']
        widgets = {
            'valor_maquineta': forms.TextInput(attrs={'id': 'valor_maquineta', 'class': 'form-control'}),
            'valor_real': forms.TextInput(attrs={'id': 'valor', 'class': 'form-control'}),
        }

    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Senha',
        required=True,
        help_text="Digite sua senha para confirmar a operação."
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Adiciona a classe 'form-control' para todos os campos do formulário
        for field in self.fields.values():
            field.widget.attrs['class'] = field.widget.attrs.get('class', '') + ' form-control'

    data_inicio = forms.DateField(
        label='Data Início',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'  # Para um seletor de data
        })
    )

    data_fim = forms.DateField(
        label='Data fim',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'  # Para um seletor de data
        })
    )

class SolicitacaoInvestimentoForm(forms.ModelForm):

    class Meta:
        model = Investimento
        fields = ['valor', 'comprovante']
        widgets = {
            'valor': forms.TextInput(attrs={'id': 'valor', 'class': 'form-control'}),
        }

    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Senha',
        required=True,
        help_text="Digite sua senha para confirmar a operação."
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Adiciona a classe 'form-control' para todos os campos do formulário
        for field in self.fields.values():
            field.widget.attrs['class'] = field.widget.attrs.get('class', '') + ' form-control'

class SolicitacaoRetiradaRendimentoForm(forms.ModelForm):

    class Meta:
        model = Retirada
        fields = ['valor', 'chave_pix', 'banco_pix', 'titular_pix']
        widgets = {
            'valor': forms.TextInput(attrs={'id': 'valor', 'class': 'form-control'}),
        }

    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Senha',
        required=True,
        help_text="Digite sua senha para confirmar a operação."
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Adiciona a classe 'form-control' para todos os campos do formulário
        for field in self.fields.values():
            field.widget.attrs['class'] = field.widget.attrs.get('class', '') + ' form-control'

class InvestimentoCartaoFinalizarForm(forms.Form):
    senha_administrador = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),  # Adicionando a classe ao widget
        required=True,
        label='Senha de Administrador'
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(InvestimentoCartaoFinalizarForm, self).__init__(*args, **kwargs)


    def clean_senha_administrador(self):
        senha = self.cleaned_data.get('senha_administrador')
        if self.user and not self.user.check_password(senha):
            raise forms.ValidationError("Senha incorreta.")
        return senha

