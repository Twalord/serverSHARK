# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-16 09:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smartshark', '0017_auto_20160613_0914'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'permissions': (('start_collection', 'Starts the collection process for projects'),)},
        ),
    ]
