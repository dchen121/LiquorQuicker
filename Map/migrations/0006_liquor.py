# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Map', '0005_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='Liquor',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('category', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=150)),
                ('size', models.DecimalField(decimal_places=3, max_digits=5)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
    ]
