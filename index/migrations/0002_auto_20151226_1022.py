# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-26 10:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='date_to_come',
            new_name='date_schedule',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='times_remain_to_clean',
            new_name='should_come_count',
        ),
    ]