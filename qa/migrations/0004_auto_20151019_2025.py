# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0003_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer_content', models.TextField(verbose_name=b'\xe5\x9b\x9e\xe7\xad\x94')),
                ('answer_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe8\xaf\x84\xe8\xae\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('pid', models.ForeignKey(verbose_name=b'\xe7\x88\xb6\xe7\xba\xa7\xe8\xaf\x84\xe8\xae\xba', blank=True, to='qa.Answer', null=True)),
                ('question', models.ForeignKey(verbose_name=b'\xe9\x97\xae\xe9\xa2\x98', to='qa.Question')),
                ('user', models.ForeignKey(verbose_name=b'\xe8\xaf\x84\xe8\xae\xba\xe7\x94\xa8\xe6\x88\xb7', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u56de\u7b54',
                'verbose_name_plural': '\u56de\u7b54',
            },
        ),
        migrations.RemoveField(
            model_name='comment',
            name='article',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='pid',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='user',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
