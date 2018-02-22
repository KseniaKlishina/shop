# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='num_items',
        ),
        migrations.AddField(
            model_name='order',
            name='good_in_order_id',
            field=models.ForeignKey(db_column=b'good_in_order', default=0, blank=True, to='website.Goods'),
            preserve_default=False,
        ),
        migrations.AlterModelTable(
            name='order',
            table='order',
        ),
    ]
