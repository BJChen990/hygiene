# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-23 16:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.TextField()),
                ('number', models.PositiveSmallIntegerField(default=0)),
                ('name', models.TextField(default=None)),
                ('type', models.TextField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_in_class', models.PositiveSmallIntegerField(default=0)),
                ('name', models.TextField(max_length=20)),
                ('gender', models.TextField(max_length=10)),
                ('student_id', models.TextField(max_length=20)),
                ('times_remain_to_clean', models.PositiveSmallIntegerField(default=3)),
                ('date_to_come', models.TextField(default='[]', max_length=60)),
                ('the_class', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='index.Class')),
            ],
        ),
    ]