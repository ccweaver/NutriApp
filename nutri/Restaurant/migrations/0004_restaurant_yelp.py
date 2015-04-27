# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurant', '0003_auto_20150327_2017'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='yelp',
            field=models.CharField(default=b'', max_length=300),
            preserve_default=True,
        ),
    ]
