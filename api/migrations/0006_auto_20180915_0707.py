# Generated by Django 2.1.1 on 2018-09-15 07:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20180915_0607'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quiz',
            old_name='value1',
            new_name='value',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='value2',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='value3',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='value4',
        ),
    ]
