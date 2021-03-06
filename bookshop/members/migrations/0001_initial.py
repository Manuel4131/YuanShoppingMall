# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2019-02-27 16:15
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VerificationCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auth_code', models.CharField(max_length=32)),
                ('expiry_date', models.DateTimeField(default=datetime.datetime(2019, 3, 3, 0, 15, 48, 100259))),
                ('user_fk', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='auth_code', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
