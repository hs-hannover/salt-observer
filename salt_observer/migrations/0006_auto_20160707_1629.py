# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-07 14:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salt_observer', '0005_auto_20160615_1439'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='minion',
            name='grains',
        ),
        migrations.AddField(
            model_name='minion',
            name='data',
            field=models.TextField(default='{}'),
        ),
    ]