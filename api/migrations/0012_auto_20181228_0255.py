# Generated by Django 2.1.4 on 2018-12-28 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20181227_1840'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='watchitem',
            options={'ordering': ['-date']},
        ),
        migrations.AddField(
            model_name='watchitem',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
