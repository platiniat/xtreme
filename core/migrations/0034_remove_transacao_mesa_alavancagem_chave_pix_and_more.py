# Generated by Django 4.2.16 on 2024-11-30 08:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_transacao_mesa_alavancagem_mesa_alavancagem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transacao_mesa_alavancagem',
            name='chave_pix',
        ),
        migrations.RemoveField(
            model_name='transacao_mesa_alavancagem',
            name='mesa_dinheiro',
        ),
        migrations.DeleteModel(
            name='Mesa_alavancagem',
        ),
        migrations.DeleteModel(
            name='Transacao_mesa_alavancagem',
        ),
    ]
