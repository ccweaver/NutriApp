# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu_items', '0004_auto_20160312_0426'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='likes',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
