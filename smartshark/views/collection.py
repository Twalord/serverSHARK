import threading
import logging
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from smartshark.common import create_substitutions_for_display, order_plugins, append_success_messages_to_req
from smartshark.datacollection.executionutils import create_jobs_for_execution
from smartshark.forms import ProjectForm, get_form, set_argument_values, set_argument_execution_values
from smartshark.models import Plugin, Project, PluginExecution, Job

from smartshark.datacollection.pluginmanagementinterface import PluginManagementInterface

logger = logging.getLogger('django')


class JobSubmissionThread(threading.Thread):
    def __init__(self, project, plugin_executions, create_jobs=True):
        threading.Thread.__init__(self)
        self.project = project
        self.plugin_executions = plugin_executions
        self.create_jobs = create_jobs

    def run(self):
        interface = PluginManagementInterface.find_correct_plugin_manager()
        jobs = []
        if self.create_jobs:
            jobs = create_jobs_for_execution(self.project, self.plugin_executions)
        interface.execute_plugins(self.project, jobs, self.plugin_executions)


def install(request):
    plugins = []

    if not request.user.is_authenticated() or not request.user.has_perm('smartshark.install_plugin'):
        messages.error(request, 'You are not authorized to perform this action.')
        return HttpResponseRedirect('/admin/smartshark/plugin')

    if not request.GET.get('ids'):
        messages.error(request, 'No plugin ids were given to install.')
        return HttpResponseRedirect('/admin/smartshark/plugin')

    for plugin_id in request.GET.get('ids', '').split(','):
        plugin = get_object_or_404(Plugin, pk=plugin_id)
        plugins.append(plugin)

    if request.method == 'POST':
        if 'cancel' in request.POST:
            return HttpResponseRedirect('/admin/smartshark/plugin')

        # create a form instance and populate it with data from the request:
        form = get_form(plugins, request.POST, 'install')
        # check whether it's valid:
        if form.is_valid():
            # Parse the fields and set the corresponding values of the install arguments in the database
            set_argument_values(form.cleaned_data)

            # Install plugins
            installations = PluginManagementInterface.find_correct_plugin_manager().install_plugins(plugins)

            # Check if plugins successfully installed
            append_success_messages_to_req(installations, plugins, request)

            return HttpResponseRedirect('/admin/smartshark/plugin')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = get_form(plugins, request.POST or None, 'install')

    return render(request, 'smartshark/plugin/install.html', {
        'form': form,
        'plugins': plugins,
        'substitutions': create_substitutions_for_display()
    })


def _check_if_at_least_one_execution_was_successful(req_plugin, project):
    # Go through all plugin executions

    tmp = req_plugin.split('_')  # one version of a plugin is enough for now
    # todo: check if version of plugin is higher than our required
    for plugin_execution in PluginExecution.objects.filter(plugin__startswith=tmp[0], project=project).all():
        if plugin_execution.was_successful():
            return True

    return False


def choose_plugins(request):
    projects = []

    if not request.user.is_authenticated() or not request.user.has_perm('smartshark.start_collection'):
        messages.error(request, 'You are not authorized to perform this action.')
        return HttpResponseRedirect('/admin/smartshark/project')

    if request.GET.get('ids'):
        for project_id in request.GET.get('ids', '').split(','):
            projects.append(get_object_or_404(Project, pk=project_id))
    else:
        messages.error(request, 'No project ids were given.')
        return HttpResponseRedirect('/admin/smartshark/project')

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        if 'cancel' in request.POST:
            return HttpResponseRedirect('/admin/smartshark/project')

        # create a form instance and populate it with data from the request:
        form = ProjectForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            plugin_ids = []
            interface = PluginManagementInterface.find_correct_plugin_manager()

            # check requirements
            for plugin in form.cleaned_data['plugins']:
                plugin_ids.append(str(plugin.id))

                # check for each plugin if required plugin is set
                '''
                missing_plugins = []
                for req_plugin in plugin.requires.all():
                    if req_plugin not in form.cleaned_data['plugins']:
                        missing_plugins.append(str(req_plugin))

                if missing_plugins:
                    messages.error(request, 'Not all requirements for plugin %s are met. Plugin(s) %s is/are required!'
                                   % (str(plugin), ', '.join(missing_plugins)))
                    return HttpResponseRedirect(request.get_full_path())
                '''
                # check if schema problems exist between plugins
                # TODO

                # if plugin with this project is in plugin execution and has status != finished | error -> problem
                for project in projects:
                    for req_plugin in plugin.requires.all():
                        logger.debug("Looking at required plugin %s" % str(req_plugin))

                        # todo: implement check for plugins taking into account the plugin version e.g., if vcsshark-0.10 is required
                        # also allow vcsshark-0.11 or newer (if info.json allows that (>=))
                        #if not _check_if_at_least_one_execution_was_successful(req_plugin, project):
                        #    messages.error(request,
                        #                   'Not all requirements for plugin %s are met. Plugin %s was not executed '
                        #                   'successfully for project %s before!'
                        #                   % (str(plugin), str(req_plugin), str(project)))
                        #    return HttpResponseRedirect(request.get_full_path())

                        logger.debug("At least one plugin execution for plugin %s was successful." % str(req_plugin))

                    # Update job information
                    plugin_executions = PluginExecution.objects.all().filter(plugin=plugin, project=project)

                    # Get all jobs from all plugin_executions which did not terminate yet
                    jobs = []
                    for plugin_execution in plugin_executions:
                        jobs.extend(Job.objects.filter(plugin_execution=plugin_execution, status='WAIT').all())

                    # Update the job stati for these jobs
                    job_stati = interface.get_job_stati(jobs)
                    i = 0
                    for job in jobs:
                        job.status = job_stati[i]
                        job.save()

                    # check if some plugin has unfinished jobs
                    has_unfinished_jobs = False
                    for plugin_execution in plugin_executions:
                        if plugin_execution.has_unfinished_jobs():
                            has_unfinished_jobs = True

                    if has_unfinished_jobs:
                        messages.error(request, 'Plugin %s is already scheduled for project %s.' % (str(plugin),
                                                                                                    project))
                        return HttpResponseRedirect(request.get_full_path())

            return HttpResponseRedirect('/smartshark/project/collection/start?plugins=%s&projects=%s' %
                                        (','.join(plugin_ids), request.GET.get('ids')))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ProjectForm()

    return render(request, 'smartshark/project/action_collection.html', {
        'form': form,
        'projects': projects,

    })


def start_collection(request):
    projects = []
    plugins = []

    if not request.user.is_authenticated() or not request.user.has_perm('smartshark.start_collection'):
        messages.error(request, 'You are not authorized to perform this action.')
        return HttpResponseRedirect('/admin/smartshark/project')

    if request.GET.get('projects'):
        for project_id in request.GET.get('projects', '').split(','):
            projects.append(get_object_or_404(Project, pk=project_id))
    else:
        messages.error(request, 'No project ids were given.')
        return HttpResponseRedirect('/admin/smartshark/project')

    if request.GET.get('plugins'):
        for plugin_id in request.GET.get('plugins', '').split(','):
            plugin = get_object_or_404(Plugin, pk=plugin_id)
            plugins.append(plugin)
    else:
        messages.error(request, 'No plugin ids were given.')
        return HttpResponseRedirect('/admin/smartshark/project')

    if request.method == 'POST':
        if 'cancel' in request.POST:
            return HttpResponseRedirect('/admin/smartshark/project')

        # create a form instance and populate it with data from the request:
        form = get_form(plugins, request.POST, 'execute')

        # check whether it's valid:
        if form.is_valid():
            execution_type = form.cleaned_data.get('execution', None)
            revisions = form.cleaned_data.get('revisions', None)
            repository_url = form.cleaned_data.get('repository_url', None)

            sorted_plugins = order_plugins(plugins)

            for project in projects:

                plugin_executions = []
                for plugin in sorted_plugins:
                    # Create Plugin Execution Objects
                    plugin_execution = PluginExecution(project=project, plugin=plugin)

                    if plugin.plugin_type == 'repo' or plugin.plugin_type == 'rev':
                        plugin_execution.repository_url = repository_url

                    if plugin.plugin_type == 'rev':
                        plugin_execution.execution_type = execution_type
                        plugin_execution.revisions = revisions

                    plugin_execution.save()
                    plugin_executions.append(plugin_execution)

                    messages.success(request, 'Started plugin %s on project %s.' %
                             (str(plugin), project.name))

                # Set execution history with execution values for the plugin execution
                set_argument_execution_values(form.cleaned_data, plugin_executions)

                # Create jobs and execute them in a separate thread
                thread = JobSubmissionThread(project, plugin_executions)
                thread.start()

            return HttpResponseRedirect('/admin/smartshark/project')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = get_form(plugins, request.POST or None, 'execute')

    return render(request, 'smartshark/project/execution.html', {
        'form': form,
        'plugins': plugins,
        'projects': projects,
        'substitutions': create_substitutions_for_display()
    })



