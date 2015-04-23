# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ingred_table', '0003_auto_20150423_1759'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredient',
            old_name='g_per_mL',
            new_name='g_per_ml',
        ),
    ]
