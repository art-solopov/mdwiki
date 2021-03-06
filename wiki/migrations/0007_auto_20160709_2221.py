# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-09 22:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0006_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='created',
            field=model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created'),
        ),
        migrations.AddField(
            model_name='comment',
            name='modified',
            field=model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='article',
            name='locale',
            field=models.SlugField(max_length=10),
        ),
        migrations.AlterField(
            model_name='historicalarticle',
            name='locale',
            field=models.SlugField(max_length=10),
        ),
    ]
