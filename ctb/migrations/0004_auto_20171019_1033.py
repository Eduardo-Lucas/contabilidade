# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-19 13:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('ctb', '0003_auto_20171019_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipodocumento',
            name='sigla',
            field=models.CharField(default='CHQ', max_length=3, unique=True),
        ),
    ]