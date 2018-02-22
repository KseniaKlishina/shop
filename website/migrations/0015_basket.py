# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('website', '0014_auto_20150519_1730'),
    ]

    operations = [
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column=b'id')),
                ('date', models.DateTimeField(verbose_name=b'date')),
                ('goods_id', models.ForeignKey(db_column=b'goods_id', to='website.Goods', null=True)),
                ('user_id', models.ForeignKey(db_column=b'user_id', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'db_table': 'basket',
            },
            bases=(models.Model,),
        ),
    ]
