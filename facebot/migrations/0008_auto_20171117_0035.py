# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-16 21:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facebot', '0007_auto_20171116_2340'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='periodpublic',
        ),
        migrations.AlterField(
            model_name='period',
            name='name',
            field=models.CharField(help_text='Уникальное имя', max_length=120, null=True, unique=True, verbose_name='Имя'),
        ),
    ]
