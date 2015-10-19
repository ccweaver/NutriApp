# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurant', '0008_auto_20150714_0422'),
        ('added_ingreds', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('valid', models.BooleanField(default=False)),
                ('description', models.TextField()),
                ('ingredients', models.ManyToManyField(to='added_ingreds.Addition', blank=True)),
                ('rest', models.ForeignKey(to='Restaurant.Restaurant')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
