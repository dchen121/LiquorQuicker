# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Map', '0007_auto_20151116_1745'),
    ]

    operations = [
        migrations.AddField(
            model_name='liquorlocation',
            name='avg_rating',
            field=models.FloatField(default=0.0),
        ),
    ]
