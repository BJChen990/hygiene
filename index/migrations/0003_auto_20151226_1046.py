# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-26 10:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0002_auto_20151226_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='date_schedule',
            field=models.TextField(default='{}', max_length=60),
        ),
    ]
