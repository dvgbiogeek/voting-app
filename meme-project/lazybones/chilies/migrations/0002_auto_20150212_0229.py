# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chilies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('date_voted', models.DateField(auto_now_add=True, null=True)),
                ('loser', models.ForeignKey(to='chilies.Meme', related_name='loser', null=True)),
                ('user_id', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
                ('winner', models.ForeignKey(to='chilies.Meme', related_name='winner', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='meme',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True),
            preserve_default=True,
        ),
    ]
