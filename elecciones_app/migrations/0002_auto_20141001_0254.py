# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elecciones_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='APoliticaUbigeo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('agrupacionPolitica', models.ForeignKey(to='elecciones_app.AgrupacionPolitica')),
                ('ambito', models.ForeignKey(to='elecciones_app.Ambito')),
                ('ubigeo', models.ForeignKey(to='elecciones_app.Ubigeo')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='acta',
            name='agrupacionPolitica',
        ),
        migrations.RemoveField(
            model_name='acta',
            name='ambito',
        ),
        migrations.RemoveField(
            model_name='acta',
            name='ubigeo',
        ),
        migrations.AddField(
            model_name='acta',
            name='APoliticaUbigeo',
            field=models.ForeignKey(default=1, to='elecciones_app.APoliticaUbigeo'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='agrupacionpolitica',
            name='ubigeo',
            field=models.ManyToManyField(to=b'elecciones_app.Ubigeo', through='elecciones_app.APoliticaUbigeo'),
        ),
    ]
