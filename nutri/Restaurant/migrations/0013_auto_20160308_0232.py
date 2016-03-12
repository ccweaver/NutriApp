# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurant', '0012_auto_20160308_0207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='cuisine1',
            field=models.CharField(max_length=110, null=True),
            preserve_default=True,
        ),
    ]
