# Generated by Django 4.2.16 on 2024-11-06 11:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_pix_agencia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pix_agencia',
            name='agencia',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='core.agencia'),
            preserve_default=False,
        ),
    ]
