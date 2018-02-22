# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advertising',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column=b'id')),
                ('description', models.TextField(db_column=b'description', blank=True)),
                ('image_id', models.ForeignKey(to='website.Image', db_column=b'image_id')),
            ],
            options={
                'db_table': 'Advertising_image',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='advertising',
            unique_together=set([('id', 'image_id')]),
        ),
    ]
