# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-02 22:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ctb', '0003_auto_20170902_1913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empresa',
            name='cnpj',
            field=models.CharField(max_length=14, unique=True, verbose_name='CNPJ'),
        ),
    ]