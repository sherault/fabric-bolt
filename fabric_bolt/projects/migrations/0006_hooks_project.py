# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_hooks'),
    ]

    operations = [
        migrations.AddField(
            model_name='hooks',
            name='project',
            field=models.ForeignKey(default=1, to='projects.Project'),
            preserve_default=False,
        ),
    ]
