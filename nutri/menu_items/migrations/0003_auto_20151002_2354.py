# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu_items', '0002_item_calories'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='carbs',
            field=models.DecimalField(default=-1, max_digits=10, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='fat',
            field=models.DecimalField(default=-1, max_digits=10, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='protein',
            field=models.DecimalField(default=-1, max_digits=10, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='sodium',
            field=models.DecimalField(default=-1, max_digits=10, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='sugar',
            field=models.DecimalField(default=-1, max_digits=10, decimal_places=2),
            preserve_default=True,
        ),
    ]
