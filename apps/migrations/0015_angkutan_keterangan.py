# Generated by Django 4.1 on 2024-08-07 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0014_penumpang_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='angkutan',
            name='keterangan',
            field=models.TextField(blank=True, null=True),
        ),
    ]
