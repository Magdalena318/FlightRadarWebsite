# Generated by Django 3.1.4 on 2021-01-13 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OpenSkyProxy', '0010_flight_adj'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flight',
            name='adj',
        ),
        migrations.AddField(
            model_name='airport',
            name='adj',
            field=models.ManyToManyField(blank=True, null=True, to='OpenSkyProxy.Waypoint'),
        ),
    ]
