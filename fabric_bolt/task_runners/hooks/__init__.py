from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from ..base import BaseTaskRunnerBackend


class BasicStreamHooksBackend(BaseTaskRunnerBackend):
    def get_detail_template(self):
        return 'task_runners/deployment_detail_basic.html'

    def get_urls(self):
        from .views import DeploymentOutputHooksStream

        return [
            url(r'^$', csrf_exempt(DeploymentOutputHooksStream.as_view()), name='projects_deployment_hooks_output'),
        ]
