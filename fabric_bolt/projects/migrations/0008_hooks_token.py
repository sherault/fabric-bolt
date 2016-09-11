# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_deployment_hook'),
    ]

    operations = [
        migrations.AddField(
            model_name='hooks',
            name='token',
            field=models.CharField(default='token', max_length=255),
            preserve_default=False,
        ),
    ]
