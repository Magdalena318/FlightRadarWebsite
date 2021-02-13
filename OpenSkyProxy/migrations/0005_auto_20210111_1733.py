# Generated by Django 3.1.4 on 2021-01-11 16:33

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('OpenSkyProxy', '0004_flight_plane'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='id',
            field=models.CharField(default=uuid.uuid4, max_length=30, primary_key=True, serialize=False, unique=True),
        ),
    ]
