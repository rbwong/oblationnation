# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oblation', '0008_auto_20150127_2141'),
        ('shop', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80)),
                ('contact', models.CharField(max_length=12)),
                ('email', models.EmailField(max_length=75)),
                ('address', models.CharField(max_length=200)),
                ('payment', models.CharField(max_length=80)),
                ('claiming', models.CharField(max_length=80)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.PositiveSmallIntegerField()),
                ('product', models.ForeignKey(to='shop.Product')),
                ('variation', models.ForeignKey(to='oblation.Variation')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(to='order.OrderProduct'),
            preserve_default=True,
        ),
    ]
