# Generated by Django 3.0.4 on 2023-05-29 18:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inscricao', '0002_auto_20230528_1819'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inscricao',
            options={'ordering': ['etapa__grupo', '-etapa__data', 'posicao_etapa', 'atleta__apelido'], 'verbose_name': 'inscrição', 'verbose_name_plural': 'inscrições'},
        ),
    ]
