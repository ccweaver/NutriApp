# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurant', '0008_auto_20150714_0422'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='neighborhood',
            field=models.CharField(default=b'', max_length=100),
            preserve_default=True,
        ),
    ]
