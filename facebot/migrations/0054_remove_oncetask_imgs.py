# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-18 18:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facebot', '0053_imageupload'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='oncetask',
            name='imgs',
        ),
    ]
