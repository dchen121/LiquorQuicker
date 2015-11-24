# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserProfile', '0007_lquser_favorite_bev'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lquser',
            name='favorite_bev',
        ),
        migrations.AddField(
            model_name='lquser',
            name='f_drink',
            field=models.CharField(null=True, max_length=150),
        ),
    ]
