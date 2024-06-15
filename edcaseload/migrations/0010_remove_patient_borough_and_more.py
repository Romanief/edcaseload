# Generated by Django 5.0.6 on 2024-06-15 11:01

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edcaseload', '0009_patient_contact_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='borough',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='discharged_hospital',
        ),
        migrations.AlterField(
            model_name='patient',
            name='dor',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='patient',
            name='first_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='patient',
            name='last_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='patient',
            name='location',
            field=models.CharField(default='blue 28', max_length=50),
        ),
        migrations.AlterField(
            model_name='patient',
            name='mrn',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]