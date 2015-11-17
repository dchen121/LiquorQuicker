# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Map', '0003_review_userreview'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserReview',
        ),
        migrations.AddField(
            model_name='review',
            name='comment',
            field=models.CharField(default='No Comment', max_length=200),
        ),
        migrations.AddField(
            model_name='review',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True, verbose_name='date published'),
        ),
        migrations.AddField(
            model_name='review',
            name='rating',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=1),
        ),
        migrations.AddField(
            model_name='review',
            name='store',
            field=models.ForeignKey(to='Map.LiquorLocation', null=True),
        ),
        migrations.AddField(
            model_name='review',
            name='user_name',
            field=models.CharField(default='baka', max_length=100),
        ),
    ]
