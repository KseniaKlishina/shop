# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('website', '0004_auto_20150509_2055'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column=b'id')),
                ('num_order', models.CharField(max_length=50, db_column=b'num_order')),
                ('adress', models.TextField(db_column=b'adress')),
                ('num_items', models.CharField(max_length=40, db_column=b'num_items', blank=True)),
                ('user_id', models.ForeignKey(db_column=b'user_id', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
