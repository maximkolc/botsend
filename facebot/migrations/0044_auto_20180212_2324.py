# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-12 20:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('facebot', '0043_auto_20180212_0137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oncetask',
            name='name',
            field=models.CharField(max_length=25, verbose_name='Имя задачи'),
        ),
        migrations.AlterUniqueTogether(
            name='oncetask',
            unique_together=set([('name', 'created_by')]),
        ),
    ]