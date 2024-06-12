from django.utils import timezone
from django.test import TestCase, Client
from django.urls import reverse
from .models import User, Patient

# Create your tests here.


class GetPatientsViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.object.create(
            username="test_user", password="test_password")

        # create patient for testing
        self.patient1 = Patient.objects.create(
            first_name='John',
            last_name='Doe',
            mrn='123456',
            borough='Brooklyn',
            doa=timezone.now(),
            location='Hospital A',
            priority=1,
            discharged_therapies=None
        )
        self.patient2 = Patient.objects.create(
            first_name='Jane',
            last_name='Doe',
            mrn='654321',
            borough='Queens',
            doa=timezone.now(),
            location='Hospital B',
            priority=2,
            discharged_therapies=timezone.now()
        )

    def test_get_patients_authorised(self):
        """
        Check that user is able to access the get_patient view correctly when logged in
        """
        self.client.login(username="test_username", password="test_password")
        response = self.client.get(reverse("edcaseload:get_patients"))
        self.assertEqual(response.status_code, 200)
        self.assertContains('Jane Doe')
        self.assertContains('John Doe')

    def test_get_patients_unauthorised(self):
        """
        Check that user is redirected to login view when trying to attempt this view when
        logged out
        """
        response = self.client.get(reverse("edcaseload:get_patients"))
        self.assertRedirects(response, reverse("edcaseload:login"))
