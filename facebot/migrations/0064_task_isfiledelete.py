# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-25 17:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facebot', '0063_auto_20180325_1930'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='isfiledelete',
            field=models.BooleanField(choices=[(True, 'Да'), (False, 'Нет')], default=False, verbose_name='Нет'),
        ),
    ]
