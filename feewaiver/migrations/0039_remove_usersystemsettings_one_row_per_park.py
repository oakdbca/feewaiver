# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-01-07 09:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feewaiver', '0038_feewaivervisit_free_parks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersystemsettings',
            name='one_row_per_park',
        ),
    ]
