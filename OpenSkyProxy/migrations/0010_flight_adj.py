# Generated by Django 3.1.4 on 2021-01-13 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OpenSkyProxy', '0009_auto_20210113_2040'),
    ]

    operations = [
        migrations.AddField(
            model_name='flight',
            name='adj',
            field=models.ManyToManyField(blank=True, null=True, to='OpenSkyProxy.Waypoint'),
        ),
    ]
