# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2018-08-24 17:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartshark', '0037_auto_20180823_2229'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='executions',
            field=models.TextField(default='Keine', editable=False),
        ),
    ]
