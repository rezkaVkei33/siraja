# Generated by Django 4.1 on 2024-08-19 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0035_kategori_trayek'),
    ]

    operations = [
        migrations.AddField(
            model_name='trayek',
            name='jumlah_armada',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
