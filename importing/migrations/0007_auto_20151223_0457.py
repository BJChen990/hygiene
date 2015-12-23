# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-23 04:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('importing', '0006_auto_20151222_0736'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='owe_date',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='student',
            name='times_has_cleaned',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='student',
            name='date_to_come',
            field=models.TextField(default='[]', max_length=60),
        ),
    ]
