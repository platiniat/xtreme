# Generated by Django 4.2.16 on 2025-01-05 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0066_alter_investimentocartao_autorizado'),
    ]

    operations = [
        migrations.AddField(
            model_name='investimentocartao',
            name='valor_prestacao',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=30, verbose_name='Valor prestação'),
        ),
    ]
