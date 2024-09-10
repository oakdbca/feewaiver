# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-06-03 04:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0021_auto_20181030_1433'),
    ]

    operations = [
        migrations.AddField(
            model_name='oracleinterfacesystem',
            name='bpoint_biller_code',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='oracleinterfacesystem',
            name='bpoint_currency',
            field=models.CharField(blank=True, default='AUD', max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='oracleinterfacesystem',
            name='bpoint_merchant_num',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='oracleinterfacesystem',
            name='bpoint_password',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='oracleinterfacesystem',
            name='bpoint_test',
            field=models.NullBooleanField(default=True),
        ),
        migrations.AddField(
            model_name='oracleinterfacesystem',
            name='bpoint_username',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='oracleinterfacesystem',
            name='integration_type',
            field=models.CharField(blank=True, choices=[('no_api', 'NO API'), ('bpoint_api', 'BPOINT API')], default='no_api', max_length=20, null=True),
        ),
    ]
