# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Map', '0005_auto_20151110_1336'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['pub_date']},
        ),
        migrations.AlterField(
            model_name='review',
            name='comment',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.IntegerField(choices=[(0, 'N/A'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=0),
        ),
    ]
