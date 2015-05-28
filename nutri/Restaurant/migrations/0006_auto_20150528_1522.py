# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurant', '0005_restaurant_delivery_min'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='delivery_min',
            field=models.DecimalField(default=0.0, max_digits=5, decimal_places=2),
            preserve_default=True,
        ),
    ]
