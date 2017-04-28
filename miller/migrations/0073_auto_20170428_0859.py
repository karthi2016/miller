# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-28 08:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miller', '0072_auto_20170421_1423'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='version',
            field=models.CharField(blank=True, default=b'', help_text=b'store the git hash for story self.contents.', max_length=22),
        ),
        migrations.AlterField(
            model_name='story',
            name='date',
            field=models.DateTimeField(auto_now_add=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='story',
            name='version',
            field=models.CharField(blank=True, default=b'', help_text=b'store the git hash for current gitted self.contents.', max_length=22),
        ),
    ]
