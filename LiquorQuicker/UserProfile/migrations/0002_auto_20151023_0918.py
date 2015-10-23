# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserProfile', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lquser',
            old_name='avitar',
            new_name='avatar',
        ),
    ]
