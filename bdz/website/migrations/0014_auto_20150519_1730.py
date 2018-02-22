# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0013_contacts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacts',
            name='email',
            field=models.CharField(max_length=40, db_column=b'email', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contacts',
            name='post',
            field=models.CharField(max_length=50, db_column=b'post'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contacts',
            name='telephone',
            field=models.TextField(db_column=b'telephone'),
            preserve_default=True,
        ),
    ]
