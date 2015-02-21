# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='remarks',
            field=models.TextField(default=datetime.datetime(2015, 2, 21, 17, 25, 53, 313195, tzinfo=utc), max_length=400),
            preserve_default=False,
        ),
    ]
