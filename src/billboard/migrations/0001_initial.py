# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notice_Model',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('creator', models.CharField(max_length=40)),
                ('text', models.CharField(max_length=400)),
                ('time_stamp', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
