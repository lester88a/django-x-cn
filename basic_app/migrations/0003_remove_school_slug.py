# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-02 20:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0002_school_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='school',
            name='slug',
        ),
    ]
