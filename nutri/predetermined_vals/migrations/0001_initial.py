# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ingred_table', '0004_auto_20150423_1801'),
    ]

    operations = [
        migrations.CreateModel(
            name='PreValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('saladGrams', models.DecimalField(max_digits=10, decimal_places=2)),
                ('wrapGrams', models.DecimalField(max_digits=10, decimal_places=2)),
                ('tomatoMozzGrams', models.DecimalField(max_digits=10, decimal_places=2)),
                ('ingredID', models.ForeignKey(to='ingred_table.Ingredient')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
