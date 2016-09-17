# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IgE',
            fields=[
                ('sequence', models.TextField(serialize=False, primary_key=True)),
                ('prediction', models.TextField()),
                ('features', models.TextField()),
                ('access', models.IntegerField()),
                ('time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='IgG1',
            fields=[
                ('sequence', models.TextField(serialize=False, primary_key=True)),
                ('prediction', models.TextField()),
                ('features', models.TextField()),
                ('access', models.IntegerField()),
                ('time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='IgG3',
            fields=[
                ('sequence', models.TextField(serialize=False, primary_key=True)),
                ('prediction', models.TextField()),
                ('features', models.TextField()),
                ('access', models.IntegerField()),
                ('time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='IgG4',
            fields=[
                ('sequence', models.TextField(serialize=False, primary_key=True)),
                ('prediction', models.TextField()),
                ('features', models.TextField()),
                ('access', models.IntegerField()),
                ('time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Immuno',
            fields=[
                ('sequence', models.TextField(serialize=False, primary_key=True)),
                ('prediction', models.TextField()),
                ('features', models.TextField()),
                ('access', models.IntegerField()),
                ('time', models.DateTimeField()),
            ],
        ),
    ]
