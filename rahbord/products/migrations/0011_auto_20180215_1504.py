# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-15 23:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_auto_20180215_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sku',
            name='sent_at',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]