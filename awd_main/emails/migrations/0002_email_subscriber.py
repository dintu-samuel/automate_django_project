# Generated by Django 5.1.1 on 2024-10-01 13:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=50)),
                ('body', models.TextField(max_length=200)),
                ('attachement', models.FileField(blank=True, upload_to='attachent_file/')),
                ('send_at', models.DateTimeField(auto_now_add=True)),
                ('email_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emails.list')),
            ],
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_address', models.EmailField(max_length=75)),
                ('email_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emails.list')),
            ],
        ),
    ]
