#!/usr/bin/env python
# -*- coding: utf-8 -*-

from smartshark.models import Job, Plugin, Project, PluginExecution

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Convenience method to set job states on multiple jobs."""

    help = 'Set job states'

    def add_arguments(self, parser):
        parser.add_argument('plugin_name', type=str)
        parser.add_argument('project_name', type=str)
        parser.add_argument('filter_state', type=str, help='Select only Jobs with this state.')
        parser.add_argument('state', type=str, help='State that will be set on Jobs.')
        parser.add_argument('--execute', action='store_true', dest='execute', help='Really execute the operation.')

    def handle(self, *args, **options):

        plugin = Plugin.objects.get(name__icontains=options['plugin_name'])
        project = Project.objects.get(name__icontains=options['project_name'])

        pe = PluginExecution.objects.get(plugin=plugin, project=project)

        jobs = Job.objects.filter(plugin_execution=pe, status=options['filter_state'].upper())

        if not options['execute']:
            self.stdout.write('not executing, to execute operation run with --execute')

        h = 'setting {} on {} jobs with state {} for plugin {} on project {}'.format(options['state'], len(jobs), options['filter_state'], plugin.name, project.name)
        self.stdout.write(h)

        if options['execute']:
            for job in jobs:
                job.status = options['state'].upper()
                job.save()

            self.stdout.write('Finished setting job states')
