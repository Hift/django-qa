# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0008_question_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='tags',
        ),
    ]
