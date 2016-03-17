# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-17 10:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('salt_observer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NetworkCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mac_address', models.CharField(max_length=17)),
                ('minion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salt_observer.Minion')),
            ],
        ),
        migrations.RenameField(
            model_name='network',
            old_name='net',
            new_name='ipv4',
        ),
        migrations.RenameField(
            model_name='network',
            old_name='subnet_mask',
            new_name='ipv4_subnet',
        ),
        migrations.AddField(
            model_name='network',
            name='ipv6',
            field=models.CharField(default='', max_length=39),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='network',
            name='ipv6_subnet',
            field=models.CharField(default='', max_length=39),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='networkcard',
            name='network',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salt_observer.Network'),
        ),
        migrations.AddField(
            model_name='minion',
            name='networks',
            field=models.ManyToManyField(through='salt_observer.NetworkCard', to='salt_observer.Network'),
        ),
    ]
