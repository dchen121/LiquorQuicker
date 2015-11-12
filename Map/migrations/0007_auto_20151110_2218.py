# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Map', '0006_liquor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='liquor',
            name='price',
            field=models.DecimalField(max_digits=7, decimal_places=2),
        ),
    ]
