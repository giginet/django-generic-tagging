# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-22 12:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='Title')),
                ('body', models.TextField(verbose_name='Body')),
            ],
        ),
    ]
