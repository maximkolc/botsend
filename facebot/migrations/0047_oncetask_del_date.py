# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-16 20:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facebot', '0046_auto_20180213_1421'),
    ]

    operations = [
        migrations.AddField(
            model_name='oncetask',
            name='del_date',
            field=models.DateTimeField(null=True, verbose_name='Время удаления'),
        ),
    ]