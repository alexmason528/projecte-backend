# Generated by Django 2.1.4 on 2018-12-24 18:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_estimation_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='estimation',
            old_name='estimation',
            new_name='value',
        ),
    ]
