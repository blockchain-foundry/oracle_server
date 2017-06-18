# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20170406_0808'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposaloraclizelink',
            name='oraclize_contract',
        ),
        migrations.RemoveField(
            model_name='proposal',
            name='address',
        ),
        migrations.RemoveField(
            model_name='proposal',
            name='links',
        ),
        migrations.RemoveField(
            model_name='proposal',
            name='source_code',
        ),
        migrations.AddField(
            model_name='keystore',
            name='is_default',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='proposal',
            name='is_state_multisig',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='ProposalOraclizeLink',
        ),
    ]
