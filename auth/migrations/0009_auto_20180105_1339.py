# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-05 13:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0008_auto_20180105_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=128, verbose_name='密码'),
        ),
    ]
