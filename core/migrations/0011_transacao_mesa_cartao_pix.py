# Generated by Django 4.2.16 on 2024-11-04 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_socio_ativo_socio_data_inicio_socio_endereco_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transacao_mesa_cartao',
            name='pix',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Chave pix'),
        ),
    ]
