# Generated by Django 5.1.4 on 2025-01-20 07:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='object_id',
            new_name='object_pk',
        ),
    ]
