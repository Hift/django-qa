# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0010_question_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='tag',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
