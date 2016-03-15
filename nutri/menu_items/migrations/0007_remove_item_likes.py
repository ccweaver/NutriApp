# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu_items', '0006_auto_20160314_2359'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='likes',
        ),
    ]
