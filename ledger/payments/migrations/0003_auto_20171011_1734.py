# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-10-11 09:34
from __future__ import unicode_literals

import django.contrib.postgres.fields.ranges
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_auto_20171004_1134'),
    ]

    operations = [
        migrations.AddField(
            model_name='oracleinterfacesystem',
            name='deduct_percentage',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='oracleinterfacesystem',
            name='percentage',
            field=django.contrib.postgres.fields.ranges.IntegerRangeField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(99), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AddField(
            model_name='oracleinterfacesystem',
            name='percentage_account_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
