# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurant', '0002_auto_20150325_0714'),
    ]

    operations = [
        migrations.RenameField(
            model_name='restaurant',
            old_name='cuisine',
            new_name='cuisine1',
        ),
        migrations.AddField(
            model_name='restaurant',
            name='cuisine2',
            field=models.CharField(max_length=110, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='cuisine3',
            field=models.CharField(max_length=110, null=True),
            preserve_default=True,
        ),
    ]
