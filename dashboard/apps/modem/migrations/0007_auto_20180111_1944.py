# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-11 19:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modem', '0006_auto_20180111_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='queue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modem.MessageQueue'),
        ),
    ]
