# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-17 19:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('institutions', '0003_auto_20171112_0636'),
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('allowregistration', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user_type', models.CharField(default='staff', editable=False, max_length=10)),
                ('deleted', models.CharField(default='N', max_length=1)),
                ('institute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staffinstitute', to='institutions.Institutions')),
                ('staffuser', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
    ]
