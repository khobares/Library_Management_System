# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-18 14:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libapp', '0004_auto_20160518_0939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libuser',
            name='phone',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='libuser',
            name='postalcode',
            field=models.CharField(blank=True, max_length=7, null=True),
        ),
    ]
