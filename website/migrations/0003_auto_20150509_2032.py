# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20150509_2021'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='advertising',
            table='Advertising',
        ),
    ]
