# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-11 18:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modem', '0003_auto_20180111_1812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='queue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modem.MessageQueue'),
        ),
    ]
