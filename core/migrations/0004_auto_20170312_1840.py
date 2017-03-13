# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-12 18:40
from __future__ import unicode_literals

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_user_site'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='settings.MEDIA_ROOT/default_images/no_avatar.png', upload_to=core.models.get_avatar_path),
        ),
    ]
