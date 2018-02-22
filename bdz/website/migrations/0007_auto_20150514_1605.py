# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_auto_20150514_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='name',
            field=models.TextField(null=True, db_column=b'name'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='sername',
            field=models.TextField(null=True, db_column=b'sername'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='town_id',
            field=models.ForeignKey(db_column=b'town', default=1, blank=True, to='website.City'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='order',
            unique_together=set([('good_in_order_id', 'town_id')]),
        ),
    ]
