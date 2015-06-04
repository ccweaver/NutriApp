# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ingred_table', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='density',
            field=models.DecimalField(default=1.0, max_digits=10, decimal_places=9),
            preserve_default=True,
        ),
    ]
