# Generated by Django 3.0.4 on 2023-06-23 17:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('etapa', '0006_auto_20230613_1705'),
        ('jogo', '0006_auto_20230622_1706'),
    ]

    operations = [
        migrations.AddField(
            model_name='jogo',
            name='etapa',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='etapa.Etapa'),
        ),
    ]
