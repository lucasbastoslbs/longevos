# Generated by Django 3.0.4 on 2023-06-11 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0005_auto_20230528_1819'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usuario',
            options={'ordering': ['-is_active', 'tipo', 'grupo', '-pontuacao', '-qtd_etapas_jogadas', 'apelido'], 'verbose_name': 'longevo', 'verbose_name_plural': 'longevos'},
        ),
        migrations.AlterField(
            model_name='usuario',
            name='data_nascimento',
            field=models.DateField(help_text='Use dd/mm/aaaa', null=True, verbose_name='Data nascimento *'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='email',
            field=models.EmailField(help_text='O email é fundamental para recuperar senha', max_length=100, null=True, verbose_name='Email '),
        ),
    ]
