# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-26 18:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('facebot', '0012_auto_20171117_1402'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Уникальное имя', max_length=120, null=True, unique=True, verbose_name='Имя')),
                ('minute', models.CharField(help_text='минута', max_length=12, null=True, verbose_name='Минута')),
                ('hour', models.CharField(help_text='Час', max_length=12, null=True, verbose_name='Час')),
                ('day', models.CharField(help_text='День', max_length=12, null=True, verbose_name='День')),
                ('month', models.CharField(help_text='Месяц', max_length=12, null=True, verbose_name='Месяц')),
                ('dayofmount', models.CharField(help_text='День недели', max_length=12, null=True, verbose_name='День недели')),
                ('task', models.ForeignKey(help_text='Задача для выполнения', null=True, on_delete=django.db.models.deletion.SET_NULL, to='facebot.Task')),
            ],
        ),
    ]
