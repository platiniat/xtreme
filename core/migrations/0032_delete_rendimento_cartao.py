# Generated by Django 4.2.16 on 2024-11-27 09:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_alter_transacao_mesa_dinheiro_data_inicio_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Rendimento_cartao',
        ),
    ]
