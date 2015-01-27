# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oblation', '0003_slides'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='is_featured',
            new_name='featured',
        ),
        migrations.AddField(
            model_name='slides',
            name='active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
