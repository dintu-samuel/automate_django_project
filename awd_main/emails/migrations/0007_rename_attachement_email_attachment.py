# Generated by Django 5.1.1 on 2024-10-10 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0006_sent'),
    ]

    operations = [
        migrations.RenameField(
            model_name='email',
            old_name='attachement',
            new_name='attachment',
        ),
    ]