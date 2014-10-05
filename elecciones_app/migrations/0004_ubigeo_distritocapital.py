# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elecciones_app', '0003_grupovotacion_contabilizado'),
    ]

    operations = [
        migrations.AddField(
            model_name='ubigeo',
            name='distritoCapital',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
