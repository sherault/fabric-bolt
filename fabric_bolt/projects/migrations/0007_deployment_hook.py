# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_hooks_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='deployment',
            name='hook',
            field=models.ForeignKey(default=None, to='projects.Hooks', null=True),
        ),
    ]
