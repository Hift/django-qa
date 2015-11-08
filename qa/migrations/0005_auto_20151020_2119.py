# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0004_auto_20151019_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='answer_content',
            field=models.TextField(max_length=10000, verbose_name=b'\xe5\x9b\x9e\xe7\xad\x94'),
        ),
        migrations.AlterField(
            model_name='question',
            name='content',
            field=models.TextField(max_length=10000, verbose_name=b'\xe5\x86\x85\xe5\xae\xb9'),
        ),
    ]
