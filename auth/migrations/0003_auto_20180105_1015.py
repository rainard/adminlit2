# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-05 02:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0002_auto_20180104_1702'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True, verbose_name='名称')),
                ('note', models.CharField(max_length=250, null=True, verbose_name='备注')),
            ],
        ),
        migrations.AlterField(
            model_name='permission',
            name='note',
            field=models.CharField(blank=True, default='无', max_length=120, null=True, verbose_name='备注'),
        ),
        migrations.AlterField(
            model_name='permission',
            name='parent_type',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='分类'),
        ),
        migrations.AddField(
            model_name='usergroup',
            name='permis',
            field=models.ManyToManyField(to='auth.Permission', verbose_name='权限'),
        ),
    ]