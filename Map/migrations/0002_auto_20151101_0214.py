# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Map', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LiquorLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('store_name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=100)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Location',
        ),
        migrations.CreateModel(
            name='BCLiquorStore',
            fields=[
                ('liquorlocation_ptr', models.OneToOneField(to='Map.LiquorLocation', primary_key=True, serialize=False, parent_link=True, auto_created=True)),
                ('post_code', models.CharField(max_length=7)),
            ],
            bases=('Map.liquorlocation',),
        ),
        migrations.CreateModel(
            name='PrivateStore',
            fields=[
                ('liquorlocation_ptr', models.OneToOneField(to='Map.LiquorLocation', primary_key=True, serialize=False, parent_link=True, auto_created=True)),
            ],
            bases=('Map.liquorlocation',),
        ),
        migrations.CreateModel(
            name='RuralAgencyStore',
            fields=[
                ('liquorlocation_ptr', models.OneToOneField(to='Map.LiquorLocation', primary_key=True, serialize=False, parent_link=True, auto_created=True)),
                ('post_code', models.CharField(max_length=7)),
            ],
            bases=('Map.liquorlocation',),
        ),
    ]
