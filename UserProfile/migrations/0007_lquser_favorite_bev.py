# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Map', '0008_liquorlocation_avg_rating'),
        ('UserProfile', '0006_auto_20151103_0011'),
    ]

    operations = [
        migrations.AddField(
            model_name='lquser',
            name='favorite_bev',
            field=models.ForeignKey(to='Map.BCLiquor', null=True),
        ),
    ]
