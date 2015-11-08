# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tagging.fields


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0005_auto_20151020_2119'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='tags',
            field=tagging.fields.TagField(max_length=255, blank=True),
        ),
    ]
