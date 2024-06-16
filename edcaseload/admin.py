from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Patient)
admin.site.register(Borough)
admin.site.register(Doctor)
admin.site.register(AdmissionReason)
admin.site.register(Discharge_locations)
