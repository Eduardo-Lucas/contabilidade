# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-24 17:25
from __future__ import unicode_literals

import ctb.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ctb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conta',
            name='codigo_conta',
            field=models.PositiveIntegerField(unique=True, validators=[ctb.models.validate_maior_que_zero], verbose_name='Código da Conta'),
        ),
    ]