# Generated by Django 3.0.4 on 2023-06-19 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foto', '0002_auto_20230619_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foto',
            name='arquivo',
            field=models.FileField(help_text='Use arquivo .png para enviar seu arquivo', upload_to='midias', verbose_name='Arquivo .png'),
        ),
    ]
