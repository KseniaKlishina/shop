# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0015_basket'),
    ]

    operations = [
        migrations.AddField(
            model_name='basket',
            name='num_items',
            field=models.CharField(max_length=40, db_column=b'num_items', blank=True),
            preserve_default=True,
        ),
    ]
