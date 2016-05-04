# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu_items', '0010_item_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.DecimalField(default=0, max_digits=10, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
