# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2018-10-16 00:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartshark', '0042_auto_20181016_0141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectmongo',
            name='executed_plugins',
            field=models.TextField(blank=True, default=None, max_length=500, null=True),
        ),
    ]
