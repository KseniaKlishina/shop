# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_auto_20150509_2032'),
    ]

    operations = [
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column=b'id')),
                ('title', models.CharField(max_length=100, db_column=b'title')),
                ('description', models.TextField(db_column=b'description', blank=True)),
                ('contents', models.TextField(db_column=b'contents', blank=True)),
                ('pub_date', models.DateTimeField(verbose_name=b'date published')),
                ('image_id', models.ForeignKey(to='website.Image', db_column=b'image_id')),
            ],
            options={
                'db_table': 'events',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='events',
            unique_together=set([('id', 'image_id')]),
        ),
    ]
