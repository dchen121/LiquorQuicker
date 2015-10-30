# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import UserProfile.models


class Migration(migrations.Migration):

    dependencies = [
        ('UserProfile', '0004_auto_20151027_1918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lquser',
            name='avatar',
            field=models.ImageField(blank=True, upload_to=UserProfile.models.avatar_directory_path),
        ),
    ]
