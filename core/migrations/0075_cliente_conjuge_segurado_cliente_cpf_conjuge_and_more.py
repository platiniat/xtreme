# Generated by Django 4.2.16 on 2025-02-08 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0074_prestacaocartao_cancelador_pagamento'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='conjuge_segurado',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Nome do Cônjuge/Segurado'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='cpf_conjuge',
            field=models.CharField(blank=True, max_length=14, null=True, verbose_name='CPF do Cônjuge/Segurado'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='data_nascimento_conjuge',
            field=models.DateField(blank=True, null=True, verbose_name='Data de Nascimento do Cônjuge/Segurado'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='telefone_conjuge',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Telefone do Cônjuge/Segurado'),
        ),
    ]
