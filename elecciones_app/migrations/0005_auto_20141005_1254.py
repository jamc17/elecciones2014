# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elecciones_app', '0004_ubigeo_distritocapital'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grupovotacion',
            name='contabilizado',
        ),
        migrations.AddField(
            model_name='acta',
            name='estado',
            field=models.SmallIntegerField(default=0),
            preserve_default=True,
        ),
    ]
