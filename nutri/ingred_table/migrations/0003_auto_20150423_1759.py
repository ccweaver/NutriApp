# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ingred_table', '0002_ingredient_density'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredient',
            old_name='density',
            new_name='g_per_mL',
        ),
    ]
