# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=300)),
                ('cuisine', models.CharField(max_length=100)),
                ('seamless', models.CharField(default=b'No', max_length=100)),
                ('number', models.IntegerField()),
                ('street', models.CharField(max_length=300)),
                ('city', models.CharField(max_length=300)),
                ('state', models.CharField(max_length=100)),
                ('zipcode', models.CharField(max_length=15)),
                ('hits', models.IntegerField(default=0)),
                ('website', models.CharField(max_length=300)),
                ('phone', models.BigIntegerField()),
                ('moopen', models.DateTimeField()),
                ('moclose', models.DateTimeField()),
                ('tuopen', models.DateTimeField()),
                ('tuclose', models.DateTimeField()),
                ('weopen', models.DateTimeField()),
                ('weclose', models.DateTimeField()),
                ('thopen', models.DateTimeField()),
                ('thclose', models.DateTimeField()),
                ('fropen', models.DateTimeField()),
                ('frclose', models.DateTimeField()),
                ('saopen', models.DateTimeField()),
                ('saclose', models.DateTimeField()),
                ('suopen', models.DateTimeField()),
                ('suclose', models.DateTimeField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'restaurant_restaurant',
            },
            bases=(models.Model,),
        ),
    ]
