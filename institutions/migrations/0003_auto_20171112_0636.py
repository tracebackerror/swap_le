# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-12 14:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0002_auto_20171005_0103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institutions',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Institute User Name'),
        ),
    ]