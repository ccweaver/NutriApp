# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ingredient', models.CharField(max_length=300)),
                ('calories', models.DecimalField(max_digits=10, decimal_places=2)),
                ('protein', models.DecimalField(max_digits=10, decimal_places=2)),
                ('fat', models.DecimalField(max_digits=10, decimal_places=2)),
                ('carbs', models.DecimalField(max_digits=10, decimal_places=2)),
                ('sugar', models.DecimalField(max_digits=10, decimal_places=2)),
                ('sodium', models.DecimalField(max_digits=10, decimal_places=2)),
                ('food_group', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
