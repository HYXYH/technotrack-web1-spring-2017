# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-27 10:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blogpost', '0010_category_color'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='post',
            name='rate',
        ),
        migrations.AlterField(
            model_name='category',
            name='color',
            field=models.CharField(choices=[('label-default', 'gray'), ('label-primary', 'blue'), ('label-success', 'green'), ('label-info', 'cyan'), ('label-warning', 'orange'), ('label-danger', 'red')], default='label-default', max_length=15),
        ),
        migrations.AddField(
            model_name='like',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likers', to='blogpost.Post'),
        ),
    ]
