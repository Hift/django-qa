# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0012_remove_user_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.FileField(default=b'avatar/default.png', upload_to=b'avatar/%Y/%m', max_length=200, blank=True, null=True, verbose_name=b'\xe5\xa4\xb4\xe5\x83\x8f'),
        ),
    ]
