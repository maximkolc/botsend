# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-28 19:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facebot', '0025_auto_20180112_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chanels',
            name='chanelname',
            field=models.CharField(help_text='Имя канала', max_length=25, unique=True, verbose_name='Имя канала'),
        ),
        migrations.AlterField(
            model_name='chanels',
            name='description',
            field=models.CharField(help_text='Описание', max_length=120, verbose_name='Описание'),
        ),
        migrations.RemoveField(
            model_name='shedule',
            name='task',
        ),
        migrations.AddField(
            model_name='shedule',
            name='task',
            field=models.ManyToManyField(help_text='Задача для выполнения', null=True, to='facebot.Task'),
        ),
    ]
