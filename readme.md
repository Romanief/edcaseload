# EDCaseload

## Table of Contents

1. Introduction
3. Technologies Used
4. Setup and Installation
5. Usage

## Introduction
This is an app built in Django to store the physiotherapy caseload in the ED through a database built in SQLite using Django models, featuring user authentication and complete database manipulation

## Technologies Used
- Backend: Django 
- Frontend: Tailwind CSS
- Database: Django Models, SQLite

## Setup and Installation
### Prerequisites
- Python (>= 3.x)
- Django (>= 3.x)
- Node.js and npm (for Tailwind CSS)
### Installation Steps
Clone the repository:

```bash
git clone https://github.com/Romanief/edcaseload
cd edcaseload
```
Set up a virtual environment:

```bash
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```
Install the required Python packages:

```bash
pip install -r requirements.txt
```

Install Node.js dependencies:

```bash
npm install
```

Set up the database:

```bash
python manage.py migrate
```

Run the development server:

```bash
python manage.py runserver
```

Compile Tailwind CSS:

```bash
npx tailwindcss -i ./src/input.css -o ./static/css/output.css --watch
```
## Usage

Create Database:

```bash
python manage.py loaddata db.json
```


Running the Development Server
```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000 in your browser to see the application running.

Running Tailwind CSS
```bash
npx tailwindcss -i ./src/input.css -o ./static/css/output.css --watch
```

Creating a Superuser
```bash
python manage.py createsuperuser
```
Access the Django admin panel at http://127.0.0.1:8000/admin.


## Styling

Tailwind CSS
Tailwind CSS is used for styling the frontend. The main Tailwind CSS file is located at src/input.css.

Example Configuration

```css
/* src/input.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom styles */
```

## Functions
Inside `views.py` you will find the logic behind my app. 
Initially the app will check if you logged in and will redirect you to either `/login` or `/getactivepatients`. 

The `login` function will return the login form template as a get request. Submitting the form will check for correct credentials and log the user in to then redirect to `/getactivepatients`. 

`get_active_patients` will load in the ED caseload, filtering the patients depending on their referral status. All the Active caseload will be displayed. `get_patients` and `pending` will render the same template with a get request but filtering only the Discharged patients or the Pending referrals. 

A post request to `pending` will change the status of the patient to either Accepted or Rejected, whilst a post request to `discharge` will discharge the patients on the caseload. 

If the user is not logged in, they can still refer a patient to the caseload through the function `refer`, with a get request it will load the form to refer a patient, by submitting the form to the same URL it will send a pending referral to the database. 


## Models

The models for this app are all around one table: 
```python

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
```

The Patient table also has a few methods: 
```python 
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
            "borough": self.borough,
            "mrn": self.mrn,
            "dao": self.doa,
            "dor": self.dor,
            "priority": self.priority,
            "discharged_therapies": self.discharged_therapies,
            "discharged_hospital": self.discharged_hospital,
            "ward": self.ward
        }
```

The method allow to accept or reject the referral, it can allow to understand if a patient is discharged through looking at its location and it allows the method to be serialized allowing the code to eventually convert it into a JSON if needed. 