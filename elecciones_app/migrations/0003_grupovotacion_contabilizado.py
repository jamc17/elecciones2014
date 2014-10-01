# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elecciones_app', '0002_auto_20141001_0254'),
    ]

    operations = [
        migrations.AddField(
            model_name='grupovotacion',
            name='contabilizado',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
