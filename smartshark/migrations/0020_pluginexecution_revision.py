# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-16 09:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartshark', '0019_auto_20160616_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='pluginexecution',
            name='revision',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
