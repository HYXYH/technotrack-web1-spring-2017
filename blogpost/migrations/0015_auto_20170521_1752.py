# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-21 17:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogpost', '0014_post_is_published'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='is_published',
        ),
        migrations.AddField(
            model_name='post',
            name='is_draft',
            field=models.BooleanField(default=False),
        ),
    ]
