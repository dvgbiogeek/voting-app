# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Meme',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=160)),
                ('pub_date', models.DateField(auto_now_add=True)),
                ('image_url', models.URLField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
