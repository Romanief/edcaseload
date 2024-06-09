from django.db import models
from django.utils import timezone

# Create your models here.


class Patient(models.Model):
    first_name = models.TextField(max_length=50)
    last_name = models.TextField(max_length=50)
    borough = models.TextField(max_length=50)
    mrn = models.TextField(max_length=50, unique=True)
    doa = models.DateField(default=timezone.now)
    dor = models.DateField()
    priority = models.IntegerField()
    location = models.TextField(default="blue 28")
    discharged_therapies = models.DateField(blank=True, null=True)
    discharged_hospital = models.DateField(blank=True, null=True)
    ward = models.IntegerField(blank=True, null=True)
    contact_time = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

    def isDischarged(self):
        return True if self.discharged_therapies or self.discharged_hospital or self.ward else False

    def serialize(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "borough": self.borough,
            "mrn": self.mrn,
            "dao": self.doa,
            "dor": self.dor,
            "priority": self.priority,
            "discharged_therapies": self.discharged_therapies,
            "discharged_hospital": self.discharged_hospital,
            "ward": self.ward
        }
