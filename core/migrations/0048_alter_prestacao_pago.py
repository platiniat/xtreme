# Generated by Django 4.2.16 on 2024-12-14 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0047_alter_retirada_valor_prestacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prestacao',
            name='pago',
            field=models.BooleanField(default=False),
        ),
    ]
