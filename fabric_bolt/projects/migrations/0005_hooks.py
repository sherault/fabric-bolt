# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20160312_1803'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hooks',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(auto_now=True)),
                ('date_deleted', models.DateTimeField(null=True, blank=True)),
                ('name', models.CharField(max_length=255)),
                ('branch', models.CharField(max_length=255)),
                ('stage', models.ForeignKey(to='projects.Stage')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
