# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurant', '0004_restaurant_yelp'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='delivery_min',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
