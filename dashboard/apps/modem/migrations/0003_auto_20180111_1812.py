# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-11 18:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modem', '0002_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageQueue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('number', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='message',
            name='queue',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='modem.MessageQueue'),
        ),
    ]
