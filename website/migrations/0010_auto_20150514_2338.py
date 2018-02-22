# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_auto_20150514_1735'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='goods_id',
            field=models.ForeignKey(db_column=b'goods_id', to='website.Goods', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='num_items',
            field=models.CharField(max_length=40, db_column=b'num_items', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='telephones',
            field=models.CharField(max_length=40, db_column=b'telephone', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='use_name',
            field=models.CharField(max_length=40, db_column=b'user_name', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='city_id',
            field=models.ForeignKey(to='website.City', db_column=b'city_id'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='order',
            unique_together=set([('goods_id', 'city_id')]),
        ),
        migrations.RemoveField(
            model_name='order',
            name='sername',
        ),
        migrations.RemoveField(
            model_name='order',
            name='name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='good_in_order_id',
        ),
    ]
