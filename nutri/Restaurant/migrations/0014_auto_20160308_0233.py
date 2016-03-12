# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurant', '0013_auto_20160308_0232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='hours',
            field=models.CharField(default=b'', max_length=300, null=True),
            preserve_default=True,
        ),
    ]
