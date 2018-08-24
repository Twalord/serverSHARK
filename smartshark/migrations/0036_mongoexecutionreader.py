# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2018-08-23 02:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smartshark', '0035_auto_20161214_1050'),
    ]

    operations = [
        migrations.CreateModel(
            name='MongoExecutionReader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smartshark.Project')),
            ],
        ),
    ]
