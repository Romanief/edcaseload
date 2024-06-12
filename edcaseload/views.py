from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.contrib.auth import authenticate, login as d_login, logout as d_logout
from django.contrib.auth.models import User

from .models import Patient

# Create your views here.


def index(request):
    """
    Returns a list containing all different links for the app
    """
    link_list = ["/get_patients", "/get_patients/[mrn]",
                 "/get_active_patients", "/refer"]
    data = {"links": []}
    for link in link_list:
        data["links"].append(link)

    return JsonResponse(data)


def get_patients(request):
    """
    Return list of all patient in the database
    """
    if not request.user.is_authenticated:
        return redirect(reverse("edcaseload:login"))

    patients = Patient.objects.all()
    context = {"patients": [
        patient for patient in patients if patient.isDischarged()]}
    return render(request, "edcaseload/caseload.html", context)


def get_active_patients(request):
    """
    Return list of all active patients
    """
    if not request.user.is_authenticated:
        return redirect(reverse("edcaseload:login"))

    patients = Patient.objects.all()
    context = {"patients": [
        patient for patient in patients if not patient.isDischarged()]}

    return render(request, "edcaseload/caseload.html", context)


def refer_patient(request):
    """
    Render the referral form, as a post request refer a patient into the caseload
    """
    if request.method == "GET":
        return render(request, "edcaseload/refer.html")

    if request.method == "POST":
        first_name = request.POST["first"]
        last_name = request.POST["last"]
        mrn = request.POST["mrn"]
        borough = request.POST["borough"]
        doa = request.POST["doa"]
        location = request.POST["location"]
        dor = timezone.now()
        priority = 1

        patient = Patient.objects.create(
            first_name=first_name,
            last_name=last_name,
            mrn=mrn,
            borough=borough,
            doa=doa,
            dor=dor,
            priority=priority,
            location=location,
        )
        patient.save()

        return redirect(reverse("edcaseload:get_active_patients"))


def discharge(request):
    """
    As a post request, discharge a patient from the therapy service
    """
    if not request.user.is_authenticated:
        return redirect(reverse("edcaseload:login"))

    if request.method == "GET":
        return redirect(reverse("edcaseload:get_active_patients"))

    if request.method == "POST":
        mrn = request.POST["mrn"]
        print(mrn)

        try:
            patient = Patient.objects.get(mrn=mrn)
            print(patient)
        except:
            return HttpResponse("Patient not found")

        patient.discharged_therapies = timezone.now()
        patient.save()

        return redirect(reverse("edcaseload:get_active_patients"))


def login(request):
    """
    Login a user
    """
    if request.method == "GET":

        # if user already logged in redirect to active caseload
        if request.user.is_authenticated:
            return redirect(reverse("edcaseload:get_active_patients"))
        return render(request, "edcaseload/login.html")

    elif request.method == "POST":
        # Get credential from form
        username = request.POST["username"]
        password = request.POST["password"]

        # Attempt to validate user
        try:
            user = authenticate(request, username=username, password=password)
        except:
            context = {"message": "Something went wrong, try again later"}
            return render(request, "edcaseload/login.html", context)

        # Attempt to login
        try:
            d_login(request, user)
        except:
            # Return error 403
            context = {"message": "Invalid credentials"}
            return render(request, "edcaseload/login.html", context)

        return redirect(reverse("edcaseload:get_active_patients"))


def register(request):
    """
    regster a new user
    """
    if request.method == "GET":
        if request.user.is_authenticated:
            logout(request)
        return render(request, "edcaseload/register.html")

    elif request.method == "POST":
        # Gather form inputs
        username = request.POST["username"]
        password = request.POST["password"]
        repeat = request.POST["repeat_password"]
        email = request.POST["email"]

        # Check form is complete in full
        if not username or not password or not repeat or not email:
            context = {"message": "Please complete form in full"}
            return render(request, "edcaseload/register.html", context)
        # Check that passwords match
        if password != repeat:
            context = {"message": "Password do not match"}
            return render(request, "edcaseload/register.html", context)

        # Create and save user
        user = User.objects.create(
            username=username, password=password, email=email)
        user.save()

        # Login user
        user = authenticate(request, username=username, password=password)
        d_login(request, user)

        return redirect(reverse("edcaseload:get_active_patients"))


def update(request, mrn):
    """
    Update a patient present in database
    """
    if request.method == "GET":
        if not request.user.is_authenticated:
            return redirect(reverse("edcaseload:login"))

        try:
            patient = Patient.objects.get(mrn=mrn)
        except:
            redirect(reverse("edcaseload:get_active_patients"))

        return render(request, "edcaseload/update.html", {"patient": patient})

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect(reverse("edcaseload:login"))

        mrn = request.POST["mrn"]

        try:
            patient = Patient.objects.get(mrn=mrn)
        except:
            redirect(reverse("edcaseload:get_active_patients"))

        first_name = request.POST["first"]
        last_name = request.POST["last"]
        borough = request.POST["borough"]
        location = request.POST["location"]
        priority = request.POST["priority"]
        contact_time = request.POST["contact_time"]

        patient.first_name = first_name
        patient.last_name = last_name
        patient.borough = borough
        patient.location = location
        patient.priority = priority
        patient.contact_time = contact_time
        patient.save()

        return redirect(reverse("edcaseload:get_active_patients"))


def logout(request):
    """
    logs out a user
    """
    d_logout(request)
    return redirect(reverse("edcaseload:login"))
