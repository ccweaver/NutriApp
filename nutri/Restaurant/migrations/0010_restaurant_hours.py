# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurant', '0009_restaurant_neighborhood'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='hours',
            field=models.CharField(default=b'', max_length=300),
            preserve_default=True,
        ),
    ]
