from django.db import models
from django.utils import timezone

# Create your models here.

BOROUGHS = [
    ("GRE", "Greenwich"),
    ("BEX", "Bexley"),
    ("LEW", "Lewisham"),
    ("HOM", "Homerton"),
    ("OOB", "Out of borough")
]
SPECIALITIES = [
    ("CAR", "Cardiology"),
    ("COE", "Geriatric"),
    ("PED", "Paediatric"),
    ("ONC", "Oncology"),
    ("ORT", "Orthopaedic"),
    ("NEU", "Neurology"),
    ("RES", "Respiratory")
]
REASONS = [
    ("FAL", "Fall"),
    ("NEU", "Neuro"),
    ("GEN", "Generally unwell"),
    ("MEH", "Mental health"),
    ("ORT", "Orthopaedic"),
    ("RES", "Respiratory")
]
LOCATION = [
    ("HOM", "Home"),
    ("WAR", "Ward"),
    ("ICB", "Rehab unit"),
    ("PLC", "Placement")
]


class Doctor(models.Model):
    name: models.CharField(max_length=50)
    speciality: models.CharField(max_length=50, default="COE")


class AdmissionReason(models.Model):
    reason: models.CharField(max_length=50, default="FAL")


class Borough(models.Model):
    Borough: models.CharField(max_length=20, default="GRE")


class Discharge_locations(models.Model):
    location: models.CharField(max_length=20, default="HOM")


class Patient(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mrn = models.CharField(max_length=50, unique=True)

    doa = models.DateField(default=timezone.now)
    dor = models.DateField(default=timezone.now)
    discharged_therapies = models.DateField(blank=True, null=True)

    priority = models.IntegerField()
    location = models.CharField(max_length=50, default="blue 28")
    ward = models.IntegerField(blank=True, null=True)
    contact_time = models.IntegerField(default=0)

    borough = models.ForeignKey(
        Borough, on_delete=models.CASCADE)
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, blank=True, null=True)
    reason = models.ForeignKey(
        AdmissionReason, on_delete=models.CASCADE)
    discharge_destination = models.ForeignKey(
        Discharge_locations, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

    def isDischarged(self):
        return True if self.discharged_therapies else False

    def serialize(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            # "borough": self.borough,
            # "mrn": self.mrn,
            # "dao": self.doa,
            # "dor": self.dor,
            # "priority": self.priority,
            # "discharged_therapies": self.discharged_therapies,
            # "discharged_hospital": self.discharged_hospital,
            # "ward": self.ward
        }
