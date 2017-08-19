# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Variation',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=20)),
                ('price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('sale_price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('activate', models.BooleanField(default=True)),
                ('inventory', models.IntegerField(null=True, blank=True)),
                ('product', models.ForeignKey(to='products.Product')),
            ],
        ),
    ]
