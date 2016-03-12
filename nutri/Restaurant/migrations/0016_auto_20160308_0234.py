# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurant', '0015_auto_20160308_0234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='phone',
            field=models.BigIntegerField(null=True),
            preserve_default=True,
        ),
    ]
