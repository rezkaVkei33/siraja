# Generated by Django 4.1 on 2024-08-02 09:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0005_penumpang_jadwal_id_penumpang'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jadwal',
            name='id_penumpang',
        ),
        migrations.AddField(
            model_name='angkutan',
            name='id_penumpang',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='apps.penumpang'),
        ),
    ]
