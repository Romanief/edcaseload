# Generated by Django 5.0.6 on 2024-06-06 16:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.TextField(max_length=50)),
                ('last_name', models.TextField(max_length=50)),
                ('borough', models.TextField(max_length=50)),
                ('mrn', models.TextField(max_length=50)),
                ('doa', models.DateField(default=datetime.datetime(2024, 6, 6, 16, 27, 48, 189715, tzinfo=datetime.timezone.utc))),
                ('dor', models.DateField()),
                ('priority', models.IntegerField()),
                ('discharged_therapies', models.DateField(null=True)),
                ('discharged_hospital', models.DateField(null=True)),
                ('ward', models.IntegerField(null=True)),
            ],
        ),
    ]
