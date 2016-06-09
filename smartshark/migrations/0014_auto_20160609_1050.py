# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-09 08:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartshark', '0013_project_clone_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='url',
            field=models.URLField(unique=True),
        ),
    ]