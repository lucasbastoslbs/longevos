# Generated by Django 3.0.4 on 2023-06-22 18:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chave', '0004_auto_20230613_1705'),
        ('jogo', '0003_auto_20230622_1019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jogo',
            name='fase',
            field=models.CharField(choices=[('CLASSIFICATÓRIA', 'Classificatória'), ('DEZESSEIS', 'Dezesseis'), ('DÉCIMA', 'Décima'), ('OITAVAS', 'Oitavas'), ('QUARTAS', 'Quartas'), ('SEMI', 'Semi'), ('FINAL', 'Final')], help_text='* Campos obrigatórios', max_length=15, verbose_name='Fase da etapa *'),
        ),
        migrations.AlterField(
            model_name='jogo',
            name='timeA',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='timeA_chave_dupla', to='chave.ChaveDupla'),
        ),
        migrations.AlterField(
            model_name='jogo',
            name='timeB',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='timeB_chave_dupla', to='chave.ChaveDupla'),
        ),
    ]
