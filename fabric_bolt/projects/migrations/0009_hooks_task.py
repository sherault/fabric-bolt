# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_hooks_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='hooks',
            name='task',
            field=models.CharField(default=b'test_env', max_length=255),
        ),
    ]
