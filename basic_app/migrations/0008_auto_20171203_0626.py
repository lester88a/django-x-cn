# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-03 06:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0007_auto_20171203_0600'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='votes',
        ),
        migrations.AddField(
            model_name='movie',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='movie',
            name='genres',
            field=models.ManyToManyField(related_name='movies', to='basic_app.Genre'),
        ),
    ]
