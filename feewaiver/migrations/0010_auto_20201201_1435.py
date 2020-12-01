# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-12-01 06:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feewaiver', '0009_park_participants'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contactdetails',
            options={'verbose_name_plural': 'Contact Details'},
        ),
        migrations.AlterModelOptions(
            name='participants',
            options={'verbose_name_plural': 'Participants'},
        ),
        migrations.AddField(
            model_name='contactdetails',
            name='participants',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='feewaiver.Participants'),
        ),
    ]
