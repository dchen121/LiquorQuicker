# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserProfile', '0003_auto_20151027_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lquser',
            name='avatar',
            field=models.ImageField(upload_to='photo/%Y/%m/%d', blank=True),
        ),
    ]
