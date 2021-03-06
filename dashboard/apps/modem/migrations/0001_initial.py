# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-08 09:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(blank=True, max_length=250, null=True)),
                ('contact', models.CharField(blank=True, max_length=250, null=True)),
                ('last_attempt', models.DateField(blank=True, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(blank=True, max_length=3, null=True)),
                ('queue', models.IntegerField()),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
