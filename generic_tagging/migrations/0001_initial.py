# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-22 08:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, unique=True, verbose_name='Label')),
            ],
            options={
                'verbose_name_plural': 'Tags',
                'verbose_name': 'Tag',
                'ordering': ('label',),
            },
        ),
        migrations.CreateModel(
            name='TaggedItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField(verbose_name='Object ID')),
                ('locked', models.BooleanField(default=False, verbose_name='Locked')),
                ('order', models.IntegerField(blank=True, default=0, verbose_name='Order')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType', verbose_name='Content type')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='generic_tagging.Tag', verbose_name='Tag')),
            ],
            options={
                'verbose_name_plural': 'Tagged items',
                'verbose_name': 'Tagged item',
                'permissions': (('lock_tagged_item', 'Can lock tagged item'), ('unlock_tagged_item', 'Can unlock tagged item')),
                'ordering': ('order', 'created_at'),
            },
        ),
        migrations.AlterUniqueTogether(
            name='taggeditem',
            unique_together=set([('tag', 'content_type', 'object_id')]),
        ),
    ]
