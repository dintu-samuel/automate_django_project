# Generated by Django 5.1.1 on 2024-10-03 19:28

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0003_alter_email_attachement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='body',
            field=ckeditor.fields.RichTextField(),
        ),
    ]