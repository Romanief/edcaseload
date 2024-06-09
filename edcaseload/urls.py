from django.urls import path

from . import views

app_name = "edcaseload"

urlpatterns = [
    path("", views.index, name="index"),
    path("getpatients", views.get_patients, name="get_patients"),
    path("getactivepatients", views.get_active_patients,
         name="get_active_patients"),
    path("refer", views.refer_patient, name="refer"),
    path("discharge", views.discharge, name="discharge"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("register", views.register, name="register"),
    path("update/<str:mrn>", views.update, name="update")
]
