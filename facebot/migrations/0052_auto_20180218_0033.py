# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-17 21:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facebot', '0051_auto_20180218_0021'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='oncetask',
            unique_together=set([]),
        ),
    ]