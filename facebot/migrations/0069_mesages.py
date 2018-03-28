# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-25 20:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facebot', '0068_auto_20180325_2220'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mesages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30, verbose_name='Имя пользователя')),
                ('text', models.CharField(max_length=200, verbose_name='Текст сообщения')),
                ('date', models.DateTimeField(verbose_name='Дата отправки')),
            ],
        ),
    ]