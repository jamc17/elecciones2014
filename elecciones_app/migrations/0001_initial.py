# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Acta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numVotos', models.IntegerField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AgrupacionPolitica',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=70)),
                ('logo', models.ImageField(null=True, upload_to=b'', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ambito',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=35)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CentroVotacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=140)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GrupoVotacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(max_length=8)),
                ('electoresHabiles', models.IntegerField(null=True, blank=True)),
                ('centroVotacion', models.ForeignKey(to='elecciones_app.CentroVotacion')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ubigeo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codDep', models.CharField(max_length=2)),
                ('codPro', models.CharField(max_length=2)),
                ('codDis', models.CharField(max_length=2)),
                ('nombre', models.CharField(max_length=70)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='centrovotacion',
            name='ubigeo',
            field=models.ForeignKey(to='elecciones_app.Ubigeo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agrupacionpolitica',
            name='ubigeo',
            field=models.ManyToManyField(to='elecciones_app.Ubigeo', through='elecciones_app.Acta'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='acta',
            name='agrupacionPolitica',
            field=models.ForeignKey(to='elecciones_app.AgrupacionPolitica'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='acta',
            name='ambito',
            field=models.ForeignKey(to='elecciones_app.Ambito'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='acta',
            name='grupoVotacion',
            field=models.ForeignKey(blank=True, to='elecciones_app.GrupoVotacion', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='acta',
            name='ubigeo',
            field=models.ForeignKey(to='elecciones_app.Ubigeo'),
            preserve_default=True,
        ),
    ]
