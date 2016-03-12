# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurant', '0010_restaurant_hours'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='frclose',
            field=models.CharField(max_length=300, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='fropen',
            field=models.CharField(max_length=300, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='moclose',
            field=models.CharField(max_length=300, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='moopen',
            field=models.CharField(max_length=300, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='saclose',
            field=models.CharField(max_length=300, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='saopen',
            field=models.CharField(max_length=300, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='suclose',
            field=models.CharField(max_length=300, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='suopen',
            field=models.CharField(max_length=300, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='thclose',
            field=models.CharField(max_length=300, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='thopen',
            field=models.CharField(max_length=300, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='tuclose',
            field=models.CharField(max_length=300, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='tuopen',
            field=models.CharField(max_length=300, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='weclose',
            field=models.CharField(max_length=300, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='weopen',
            field=models.CharField(max_length=300, null=True),
            preserve_default=True,
        ),
    ]
