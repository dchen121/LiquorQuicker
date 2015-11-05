# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Map', '0002_auto_20151101_0214'),
        ('UserProfile', '0005_auto_20151030_1611'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lquser',
            name='screen_name',
        ),
        migrations.AddField(
            model_name='lquser',
            name='favorite_store',
            field=models.ForeignKey(to='Map.LiquorLocation', null=True),
        ),
    ]
