# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notice_model',
            name='file_path',
            field=models.CharField(max_length=250, blank=True, default=None, null=True),
            preserve_default=True,
        ),
    ]
