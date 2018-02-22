# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0010_auto_20150514_2338'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='order',
            unique_together=set([]),
        ),
    ]
