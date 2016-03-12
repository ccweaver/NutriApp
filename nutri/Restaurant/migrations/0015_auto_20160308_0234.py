# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurant', '0014_auto_20160308_0233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='website',
            field=models.CharField(max_length=300, null=True),
            preserve_default=True,
        ),
    ]
