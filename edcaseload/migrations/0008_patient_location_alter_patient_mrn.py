# Generated by Django 5.0.6 on 2024-06-09 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edcaseload', '0007_alter_patient_discharged_hospital_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='location',
            field=models.TextField(default='blue 28'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='mrn',
            field=models.TextField(max_length=50, unique=True),
        ),
    ]
