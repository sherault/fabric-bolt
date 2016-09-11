from django.conf import settings
from django.utils.module_loading import import_string

__author__ = 'jproffitt'


def get_backend():
    backend_class = import_string(settings.TASK_RUNNER_BACKEND)
    return backend_class()


def get_hooks():
    hooks_class = import_string('fabric_bolt.task_runners.hooks.BasicStreamHooksBackend')
    return hooks_class()

backend = get_backend()

hooks = get_hooks()
