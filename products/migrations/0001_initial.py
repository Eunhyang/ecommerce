# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=20)),
                ('description', models.TextField(null=True, blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('activate', models.BooleanField(default=True)),
            ],
        ),
    ]
