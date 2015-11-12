# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Map', '0007_auto_20151110_2218'),
    ]

    operations = [
        migrations.CreateModel(
            name='BCLiquor',
            fields=[
                ('liquor_ptr', models.OneToOneField(primary_key=True, auto_created=True, to='Map.Liquor', parent_link=True, serialize=False)),
            ],
            bases=('Map.liquor',),
        ),
        migrations.CreateModel(
            name='PrivateLiquor',
            fields=[
                ('liquor_ptr', models.OneToOneField(primary_key=True, auto_created=True, to='Map.Liquor', parent_link=True, serialize=False)),
                ('store', models.ForeignKey(to='Map.PrivateStore')),
            ],
            bases=('Map.liquor',),
        ),
        migrations.CreateModel(
            name='RASLiquor',
            fields=[
                ('liquor_ptr', models.OneToOneField(primary_key=True, auto_created=True, to='Map.Liquor', parent_link=True, serialize=False)),
                ('store', models.ForeignKey(to='Map.RuralAgencyStore')),
            ],
            bases=('Map.liquor',),
        ),
    ]
