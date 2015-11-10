# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Map', '0002_auto_20151101_0214'),
    ]

    operations = [
        migrations.RenameField(
            model_name='liquorlocation',
            old_name='store_name',
            new_name='name',
        ),
    ]
