from django.core.urlresolvers import reverse
from django.db import models

from core.mixins.models import TrackingFields


class ProjectType(TrackingFields):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return '%s' % self.name


class Project(TrackingFields):
    """Model for a project (pretty obvious)

    Keeps track of the stages and general configurations for deployments"""

    name = models.CharField(max_length=255)

    type = models.ForeignKey(ProjectType, blank=True, null=True)

    description = models.TextField(blank=True, null=True)

    # Misc information for a project
    number_of_deployments = models.IntegerField(default=0)

    def __unicode__(self):
        return '%s' % self.name

    def get_absolute_url(self):
        return reverse('projects_project_view', args=(self.pk,))


class Configuration(TrackingFields):
    project = models.ForeignKey(Project)

    key = models.CharField(max_length=255)
    value = models.CharField(max_length=500)

    def __unicode__(self):
        return '%s: %s' % (self.key, self.value)

