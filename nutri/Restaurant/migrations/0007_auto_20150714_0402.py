# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurant', '0006_auto_20150528_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='moopen',
            field=models.CharField(max_length=300),
            preserve_default=True,
        ),
    ]
