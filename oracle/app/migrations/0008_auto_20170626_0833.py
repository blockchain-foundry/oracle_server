# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20170611_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='multisig_address',
            field=models.CharField(blank=True, unique=True, max_length=100),
        ),
    ]
