# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Map', '0004_auto_20151110_1228'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, default=-1),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=0),
        ),
    ]
