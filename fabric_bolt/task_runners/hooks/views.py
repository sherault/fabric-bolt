import json

from django.contrib.sessions.backends.db import SessionStore
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View

from fabric_bolt.projects import models
from stronghold.decorators import public
from django.utils.decorators import method_decorator
from fabric_bolt.accounts.models import DeployUser

from pprint import pprint
from django.test import RequestFactory

from fabric_bolt.task_runners.basic.views import DeploymentOutputStream


class ExecuteDeploymentResponse(HttpResponse):

    def close(self):
        super(ExecuteDeploymentResponse, self).close()
        # do whatever you want, this is the last codepoint in request handling
        if self.status_code == 200:
            self.executeDeploy()

    def setInfos(self, request, stage, hooks):
        self.stage = stage
        self.hooks = hooks
        self.request = request

    def executeDeploy(self):
        body_unicode = self.request.body.decode('utf-8')
        body = json.loads(body_unicode)
        if body['ref'] != self.hooks.branch:
            print "Hooks does'nt match pushed branch."
            return
        description = "Push initiator:\r\n"
        description += body['user_name'] + " <" + body['user_email'] + ">\r\n\r\n"
        description += "Number of commits: " + str(body['total_commits_count']) + "\r\n\r\n"
        description += "Commits details:\r\n"
        for idx, commit in enumerate(body['commits']):
            description += "Commit " + str(idx + 1) + " :\r\n"
            description += "\tAuthor: " + commit['author']['name'] + " <" + commit['author']['email'] + ">\r\n"
            description += "\tMessage: " + commit['message'] + "\r\n"
            if len(commit['added']) > 0:
                description += "\tFile(s) added:\r\n"
                for added in commit['added']:
                    description += "\t\t- " + added + "\r\n"

            if len(commit['modified']) > 0:
                description += "\tFile(s) modified:\r\n"
                for modified in commit['modified']:
                    description += "\t\t- " + modified + "\r\n"

            if len(commit['removed']) > 0:
                description += "\tFile(s) removed:\r\n"
                for removed in commit['removed']:
                    description += "\t\t- " + removed + "\r\n"
            description += "\r\n"

        print description
        deployment = models.Deployment()

        # Check if User exists, otherwise, create it
        try:
            user = DeployUser.objects.get(email=body['user_email'])
        except:
            user = DeployUser.objects.create_user(body['user_email'])

        deployment.user = user
        deployment.comments = description
        deployment.stage = self.stage
        deployment.hook = self.hooks
        deployment.task, created = models.Task.objects.get_or_create(
            name=self.hooks.task,
            defaults={'description': self.hooks.task}
        )

        if not created:
            deployment.task.times_used += 1
            deployment.task.description = self.hooks.task
            deployment.task.save()

        deployment.save()

        url = reverse('projects_deployment_output', args=(self.hooks.project.pk, self.stage.pk, deployment.pk))

        request_factory = RequestFactory()
        my_request = request_factory.get(url)
        my_request.user = user
        my_request.session = SessionStore()
        my_request.session.create()

        response = DeploymentOutputStream.as_view()(my_request, project_id=self.hooks.project.pk, stage_id=self.stage.pk, pk=deployment.pk)
        pprint(response)
        pprint(response.streaming_content)

        for line in response.streaming_content:
            print line


class DeploymentOutputHooksStream(View):
    """
    Deployment view does the heavy lifting of calling Fabric Task for a Project Stage
    """
    model = models.Hooks

    @method_decorator(public)
    def dispatch(self, request, *args, **kwargs):
        self.stage = get_object_or_404(models.Stage, id=kwargs['stage_id'])
        self.hook = get_object_or_404(models.Hooks, stage=self.stage, token=kwargs['token'])

        return super(DeploymentOutputHooksStream, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DeploymentOutputHooksStream, self).get_context_data(**kwargs)
        context['project'] = self.project

        return context

    def post(self, request, *args, **kwargs):
        resp = ExecuteDeploymentResponse('toto')
        resp.setInfos(request, self.stage, self.hook)

        return resp
