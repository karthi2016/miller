# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-13 15:04
from __future__ import unicode_literals

import django.contrib.postgres.search
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('miller', 'enable_psql_extensions'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='search_vector',
            field=django.contrib.postgres.search.SearchVectorField(null=True),
        ),
    ]
