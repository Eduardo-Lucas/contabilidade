# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-02 22:13
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ctb', '0002_auto_20170824_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empresa',
            name='cnpj',
            field=models.PositiveIntegerField(unique=True, validators=[django.core.validators.MaxValueValidator(99999999999999)], verbose_name='CNPJ'),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='municipio',
            field=models.ForeignKey(default=2927408, on_delete=django.db.models.deletion.CASCADE, to='glb.GlobalMunicipio'),
        ),
    ]
