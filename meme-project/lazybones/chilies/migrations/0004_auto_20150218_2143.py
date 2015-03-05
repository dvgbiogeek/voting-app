# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chilies', '0003_auto_20150212_0551'),
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('meme_id', models.ForeignKey(to='chilies.Meme')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='meme',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='vote',
            name='date_voted',
            field=models.DateTimeField(null=True, auto_now_add=True),
            preserve_default=True,
        ),
    ]
