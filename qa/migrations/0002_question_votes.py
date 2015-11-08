# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='votes',
            field=models.IntegerField(default=0, verbose_name=b'\xe7\xa5\xa8\xe6\x95\xb0'),
        ),
    ]
