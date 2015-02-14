# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oblation', '0008_auto_20150127_2141'),
    ]

    operations = [
        migrations.CreateModel(
            name='Claiming',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='item',
            name='claiming',
            field=models.ManyToManyField(to='oblation.Claiming'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='payment',
            field=models.ManyToManyField(to='oblation.Payment'),
            preserve_default=True,
        ),
    ]
