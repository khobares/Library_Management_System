# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-14 15:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libapp', '0009_auto_20160614_1000'),
    ]

    operations = [
        migrations.AddField(
            model_name='suggestion',
            name='title',
            field=models.CharField(default=2, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='suggestion',
            name='comments',
            field=models.TextField(blank=True, null=True),
        ),
    ]
