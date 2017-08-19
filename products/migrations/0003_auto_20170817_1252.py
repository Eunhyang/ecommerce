# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_variation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=120),
        ),
        migrations.AlterField(
            model_name='variation',
            name='sale_price',
            field=models.DecimalField(decimal_places=2, blank=True, null=True, max_digits=20),
        ),
        migrations.AlterField(
            model_name='variation',
            name='title',
            field=models.CharField(max_length=120),
        ),
    ]
