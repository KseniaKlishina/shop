# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_auto_20150514_1605'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='town_id',
            new_name='cyty_id',
        ),
        migrations.AlterUniqueTogether(
            name='order',
            unique_together=set([('good_in_order_id', 'cyty_id')]),
        ),
    ]
