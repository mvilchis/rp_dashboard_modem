# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-11 20:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modem', '0007_auto_20180111_1944'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='status',
            field=models.CharField(blank=True, choices=[('N', 'N'), ('C', 'C')], max_length=3, null=True),
        ),
    ]