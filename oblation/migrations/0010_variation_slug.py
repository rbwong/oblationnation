# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('oblation', '0009_auto_20150209_2328'),
    ]

    operations = [
        migrations.AddField(
            model_name='variation',
            name='slug',
            field=models.CharField(default=datetime.datetime(2015, 2, 11, 17, 26, 11, 430773, tzinfo=utc), max_length=80),
            preserve_default=False,
        ),
    ]
