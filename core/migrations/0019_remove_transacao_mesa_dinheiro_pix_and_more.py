# Generated by Django 4.2.16 on 2024-11-07 09:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_alter_transacao_mesa_dinheiro_pix'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transacao_mesa_dinheiro',
            name='pix',
        ),
        migrations.AddField(
            model_name='transacao_mesa_dinheiro',
            name='chave_pix',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.pix_agencia', verbose_name='Chave Pix'),
        ),
    ]
