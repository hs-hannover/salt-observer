# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-22 08:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salt_observer', '0017_networkinterface_ip_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domain',
            name='md_content',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='domain',
            name='md_last_edited',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='minion',
            name='md_content',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='minion',
            name='md_last_edited',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='network',
            name='md_content',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='network',
            name='md_last_edited',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]