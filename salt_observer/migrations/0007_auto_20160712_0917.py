# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-12 07:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salt_observer', '0006_auto_20160707_1629'),
    ]

    operations = [
        migrations.RenameField(
            model_name='minion',
            old_name='data',
            new_name='_data',
        ),
    ]