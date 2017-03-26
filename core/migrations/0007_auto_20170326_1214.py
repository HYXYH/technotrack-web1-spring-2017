# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-26 12:14
from __future__ import unicode_literals

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20170312_1924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=core.models.get_avatar_path),
        ),
    ]
