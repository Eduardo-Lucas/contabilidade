# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-20 14:02
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('ctb', '0009_auto_20171219_1840'),
    ]

    operations = [
        migrations.AddField(
            model_name='processo',
            name='modulo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ctb.Modulo'),
        ),
        migrations.AddField(
            model_name='tipomovimento',
            name='modulo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ctb.Modulo'),
        ),
        migrations.AlterField(
            model_name='modulo',
            name='descricao',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
