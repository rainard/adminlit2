# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-05 04:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0004_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='data_joined',
            field=models.DateTimeField(auto_created=True, null=True, verbose_name='加入日期'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, null=True, verbose_name='邮箱'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=64, null=True, verbose_name='姓'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='有效'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, verbose_name='运维'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False, verbose_name='超级用户'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(null=True, verbose_name='最后登录'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=64, null=True, verbose_name='名'),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=120, verbose_name='密码'),
        ),
        migrations.AlterField(
            model_name='user',
            name='usergroup',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auth.UserGroup', verbose_name='用户组'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=64, unique=True, verbose_name='用户名'),
        ),
    ]
