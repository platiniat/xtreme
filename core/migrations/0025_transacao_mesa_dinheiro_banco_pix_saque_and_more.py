# Generated by Django 4.2.16 on 2024-11-10 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_transacao_mesa_dinheiro_chave_pix_saque'),
    ]

    operations = [
        migrations.AddField(
            model_name='transacao_mesa_dinheiro',
            name='banco_pix_saque',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='transacao_mesa_dinheiro',
            name='nome_pix_saque',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
