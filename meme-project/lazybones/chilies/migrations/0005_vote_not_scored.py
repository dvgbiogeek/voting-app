# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chilies', '0004_auto_20150218_2143'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='not_scored',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
