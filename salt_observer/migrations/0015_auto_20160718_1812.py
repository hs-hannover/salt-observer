# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-18 16:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salt_observer', '0014_domain_md_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domain',
            name='md_content',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='minion',
            name='md_content',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='network',
            name='md_content',
            field=models.TextField(blank=True),
        ),
    ]
