# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-28 13:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smartshark', '0031_auto_20161027_1430'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExecutionHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('execution_value', models.CharField(blank=True, default=None, max_length=300, null=True)),
            ],
        ),
        migrations.RenameField(
            model_name='argument',
            old_name='value',
            new_name='install_value',
        ),
        migrations.RemoveField(
            model_name='plugin',
            name='abstraction_level',
        ),
        migrations.AddField(
            model_name='plugin',
            name='linux_libraries',
            field=models.CharField(blank=True, default=None, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='plugin',
            name='plugin_type',
            field=models.CharField(choices=[('rev', 'Revision'), ('repo', 'Repository'), ('other', 'Other'), ('analysis', 'Analysis')], default=None, max_length=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='executionhistory',
            name='execution_argument',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smartshark.Argument'),
        ),
        migrations.AddField(
            model_name='executionhistory',
            name='plugin_execution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smartshark.PluginExecution'),
        ),
    ]
