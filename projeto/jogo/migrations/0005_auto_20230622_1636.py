# Generated by Django 3.0.4 on 2023-06-22 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jogo', '0004_auto_20230622_1535'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jogo',
            options={'ordering': ['fase'], 'verbose_name': 'jogo', 'verbose_name_plural': 'jogos'},
        ),
    ]