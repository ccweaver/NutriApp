# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu_items', '0003_auto_20151002_2354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='calories',
            field=models.DecimalField(default=0, null=True, max_digits=10, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='item',
            name='carbs',
            field=models.DecimalField(default=-1, null=True, max_digits=10, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='item',
            name='fat',
            field=models.DecimalField(default=-1, null=True, max_digits=10, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='item',
            name='protein',
            field=models.DecimalField(default=-1, null=True, max_digits=10, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='item',
            name='sodium',
            field=models.DecimalField(default=-1, null=True, max_digits=10, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='item',
            name='sugar',
            field=models.DecimalField(default=-1, null=True, max_digits=10, decimal_places=2),
            preserve_default=True,
        ),
    ]
