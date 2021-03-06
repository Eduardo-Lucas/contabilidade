# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-15 19:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('ctb', '0006_auto_20171019_1045'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lancamentocontabil',
            options={'ordering': ['-id'], 'verbose_name': 'Lançamento Contábil',
                     'verbose_name_plural': 'Lançamentos Contábeis (Lançamentos)'},
        ),
        migrations.AlterModelOptions(
            name='movimentocontabilheader',
            options={'ordering': ['-id'], 'verbose_name': 'Movimento Contábil',
                     'verbose_name_plural': 'Movimentos Contábeis (Header)'},
        ),
        migrations.AlterModelOptions(
            name='saldocontacontabil',
            options={'ordering': ['conta', '-data_competencia'], 'verbose_name': 'Saldo da Conta Contábil',
                     'verbose_name_plural': 'Saldos das Contas Contábeis'},
        ),
        migrations.AddField(
            model_name='empresa',
            name='sigla',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Sigla'),
        ),
        migrations.AlterField(
            model_name='lancamentocontabil',
            name='d_c',
            field=models.CharField(choices=[('D', 'Débito'), ('C', 'Crédito')], default='D', max_length=1,
                                   verbose_name='D/C'),
        ),
    ]
