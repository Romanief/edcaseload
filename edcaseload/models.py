from django.db import models
from django.utils import timezone

# Create your models here.


BOROUGHS = [
    ("Greenwich", "Greenwich"),
    ("Bexley", "Bexley"),
    ("Lewisham", "Lewisham"),
    ("Homerton", "Homerton"),
    ("Out of borough", "Out of borough")
]
SPECIALITIES = [
    ("Cardiology", "Cardiology"),
    ("Geriatric", "Geriatric"),
    ("Paediatric", "Paediatric"),
    ("Oncology", "Oncology"),
    ("Orthopaedic", "Orthopaedic"),
    ("Neurology", "Neurology"),
    ("Respiratory", "Respiratory")
]
REASONS = [
    ("Fall", "Fall"),
    ("Neuro", "Neuro"),
    ("Generally unwell", "Generally unwell"),
    ("Mental Health", "Mental health"),
    ("Orthopaedic", "Orthopaedic"),
    ("Respiratory", "Respiratory")
]
LOCATIONS = [
    ("Home", "Home"),
    ("Ward", "Ward"),
    ("Rehab unit", "Rehab unit"),
    ("Placement", "Placement")
]
REFERRALS_STATUS = [
    ("Pending", "Pending"),
    ("Accepted", "Accepted"),
    ("Rejected", "Rejected")
]


class Doctor(models.Model):
    name = models.CharField(max_length=50)
    speciality = models.CharField(max_length=50, choices=SPECIALITIES)

    def __str__(self):
        return self.name


class AdmissionReason(models.Model):
    reason = models.CharField(max_length=50, choices=REASONS)
    
    def __str__(self):
        return self.reason


class Borough(models.Model):
    borough = models.CharField(max_length=20, choices=BOROUGHS)

    def __str__(self):
        return self.borough


class Discharge_location(models.Model):
    location = models.CharField(max_length=20, choices=LOCATIONS)

    def __str__(self):
        return self.location


# class Referral(models.Model):
#     status = models.CharField(max_length=20, choices=REFERRALS_STATUS)

#     def accept_referral(self): 
#         if self.status != "Pending": return print("Invalid action")
#         self.status = "Accepted"
    
#     def reject_referral(self):   
#         if self.status != "Pending": return print("Invalid action")
#         self.status = "Rejected"

#     def __str__(self):
#         return self.status


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

    borough = models.ForeignKey(Borough, on_delete=models.CASCADE, default=1)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, blank=True, null=True)
    reason = models.ForeignKey(AdmissionReason, on_delete=models.CASCADE, default=1)
    discharge_destination = models.ForeignKey(Discharge_location, on_delete=models.CASCADE, default=1)
    referral = models.CharField(choices=REFERRALS_STATUS, default="Pending", max_length=20)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"
    
    def accept_referral(self):
        self.referral = "Accepted"
    
    def reject_referral(self):
        self.referral = "Rejected"

    def isDischarged(self):
        return True if self.discharged_therapies else False

    def serialize(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            # "borough": self.borough,
            "mrn": self.mrn,
            "dao": self.doa,
            "dor": self.dor,
            # "priority": self.priority,
            # "discharged_therapies": self.discharged_therapies,
            # "discharged_hospital": self.discharged_hospital,
            # "ward": self.ward
        }
