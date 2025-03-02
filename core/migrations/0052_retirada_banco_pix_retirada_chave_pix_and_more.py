# Generated by Django 4.2.16 on 2024-12-23 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0051_investimento_reinvestido'),
    ]

    operations = [
        migrations.AddField(
            model_name='retirada',
            name='banco_pix',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Banco'),
        ),
        migrations.AddField(
            model_name='retirada',
            name='chave_pix',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Chave pix'),
        ),
        migrations.AddField(
            model_name='retirada',
            name='titular_pix',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Titular'),
        ),
    ]
