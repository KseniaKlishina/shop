# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_auto_20150514_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='city_id',
            field=models.ForeignKey(db_column=b'city', default=1, blank=True, to='website.City'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='order',
            unique_together=set([('good_in_order_id', 'city_id')]),
        ),
        migrations.RemoveField(
            model_name='order',
            name='cyty_id',
        ),
    ]
