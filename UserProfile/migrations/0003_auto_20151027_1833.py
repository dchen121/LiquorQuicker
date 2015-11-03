# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserProfile', '0002_auto_20151023_0918'),
    ]

    operations = [
        migrations.AddField(
            model_name='lquser',
            name='screen_name',
            field=models.CharField(default='anon', max_length=100),
        ),
        migrations.AlterField(
            model_name='lquser',
            name='avatar',
            field=models.ImageField(upload_to='profile_images', verbose_name='photos/%Y/%m/%d', blank=True),
        ),
    ]
