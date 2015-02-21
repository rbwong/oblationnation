# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_order_remarks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='remarks',
            field=models.TextField(max_length=400, null=True, blank=True),
            preserve_default=True,
        ),
    ]
