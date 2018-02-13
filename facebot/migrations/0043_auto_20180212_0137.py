# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-11 22:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('facebot', '0042_oncetask_run_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='oncetask',
            name='bottoken',
            field=models.ForeignKey(help_text='Бот для выполнения задачи', null=True, on_delete=django.db.models.deletion.SET_NULL, to='facebot.MyBot'),
        ),
        migrations.AddField(
            model_name='oncetask',
            name='chanelforpublic',
            field=models.ForeignKey(help_text='Канал для публикации', null=True, on_delete=django.db.models.deletion.SET_NULL, to='facebot.Chanels'),
        ),
        migrations.AddField(
            model_name='oncetask',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='oncetask',
            name='run_date',
            field=models.DateTimeField(null=True, verbose_name='Время запуска'),
        ),
    ]
