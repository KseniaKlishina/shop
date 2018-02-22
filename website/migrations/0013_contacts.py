# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0012_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column=b'id')),
                ('post', models.CharField(max_length=50, db_column=b'num_order')),
                ('telephone', models.TextField(db_column=b'adress')),
                ('email', models.CharField(max_length=40, db_column=b'user_name', blank=True)),
            ],
            options={
                'db_table': 'contacts',
            },
            bases=(models.Model,),
        ),
    ]
