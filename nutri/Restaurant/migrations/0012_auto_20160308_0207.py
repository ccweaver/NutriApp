# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurant', '0011_auto_20160308_0205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='yelp',
            field=models.CharField(default=b'', max_length=300, null=True),
            preserve_default=True,
        ),
    ]
