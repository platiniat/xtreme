# Generated by Django 4.2.16 on 2024-11-07 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_pix_agencia_cpf_cnpj'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transacao_mesa_dinheiro',
            name='pix',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.pix_agencia', verbose_name='Chave pix'),
        ),
    ]
