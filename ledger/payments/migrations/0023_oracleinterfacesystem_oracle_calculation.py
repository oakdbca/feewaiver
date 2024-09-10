# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-06-08 07:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0022_auto_20210603_1233'),
    ]

    operations = [
        migrations.AddField(
            model_name='oracleinterfacesystem',
            name='oracle_calculation',
            field=models.CharField(blank=True, choices=[('version_1', 'Version 1'), ('version_2', 'Version 2')], default='version_1', max_length=20, null=True),
        ),
    ]
