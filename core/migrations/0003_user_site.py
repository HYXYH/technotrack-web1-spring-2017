# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-12 18:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20170312_1443'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='site',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
