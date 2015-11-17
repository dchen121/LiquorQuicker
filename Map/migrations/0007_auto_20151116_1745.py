# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Map', '0006_auto_20151111_1529'),
    ]

    operations = [
        migrations.CreateModel(
            name='Liquor',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('category', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=150)),
                ('size', models.DecimalField(decimal_places=3, max_digits=5)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
            ],
        ),
        migrations.RenameField(
            model_name='liquorlocation',
            old_name='store_name',
            new_name='name',
        ),
        migrations.CreateModel(
            name='BCLiquor',
            fields=[
                ('liquor_ptr', models.OneToOneField(to='Map.Liquor', serialize=False, primary_key=True, auto_created=True, parent_link=True)),
            ],
            bases=('Map.liquor',),
        ),
        migrations.CreateModel(
            name='PrivateLiquor',
            fields=[
                ('liquor_ptr', models.OneToOneField(to='Map.Liquor', serialize=False, primary_key=True, auto_created=True, parent_link=True)),
                ('store', models.ForeignKey(to='Map.PrivateStore')),
            ],
            bases=('Map.liquor',),
        ),
        migrations.CreateModel(
            name='RASLiquor',
            fields=[
                ('liquor_ptr', models.OneToOneField(to='Map.Liquor', serialize=False, primary_key=True, auto_created=True, parent_link=True)),
                ('store', models.ForeignKey(to='Map.RuralAgencyStore')),
            ],
            bases=('Map.liquor',),
        ),
    ]
