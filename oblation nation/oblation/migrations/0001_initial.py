# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('product_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='shop.Product')),
                ('description', models.TextField(null=True, blank=True)),
                ('image', models.ImageField(upload_to=b'merchandise/')),
                ('is_featured', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=('shop.product',),
        ),
    ]
