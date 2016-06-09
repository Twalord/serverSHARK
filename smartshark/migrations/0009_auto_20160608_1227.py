# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-08 10:27
from __future__ import unicode_literals

from django.db import migrations, models
import smartshark.models


class Migration(migrations.Migration):

    dependencies = [
        ('smartshark', '0008_auto_20160608_1002'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plugin',
            name='definition',
        ),
        migrations.RemoveField(
            model_name='plugin',
            name='schema',
        ),
        migrations.AddField(
            model_name='argument',
            name='description',
            field=models.CharField(default=None, max_length=250),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='plugin',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='plugin',
            name='archive',
            field=models.FileField(upload_to='uploads/plugins/', validators=[smartshark.models.FileValidator(content_types=('application/x-tar', 'application/octet-stream'), max_size=52428800)]),
        ),
        migrations.AlterField(
            model_name='plugin',
            name='installed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='plugin',
            name='requires',
            field=models.ManyToManyField(blank=True, related_name='_plugin_requires_+', to='smartshark.Plugin'),
        ),
    ]