from django.utils import timezone
from django.test import TestCase, Client
from django.urls import reverse
from .models import Patient
from django.contrib.auth.models import User

# Create your tests here.


class GetPatientsViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username="test_user", password="test_password")

        # create patient for testing
        self.patient1 = Patient.objects.create(
            first_name='John',
            last_name='Doe',
            mrn='123456',
            borough='Brooklyn',
            doa=timezone.now(),
            dor=timezone.now(),
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
            dor=timezone.now(),
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


class GetActivePatientsViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username="test_user", password="test_password")

        # create patient for testing
        self.patient1 = Patient.objects.create(
            first_name='John',
            last_name='Doe',
            mrn='123456',
            borough='Brooklyn',
            doa=timezone.now(),
            dor=timezone.now(),
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
            dor=timezone.now(),
            location='Hospital B',
            priority=2,
            discharged_therapies=timezone.now()
        )

    def test_get_active_patients_authorised(self):
        """
        Check that user is able to access the get_patient view correctly when logged in
        """
        self.client.login(username="test_username", password="test_password")
        response = self.client.get(reverse("edcaseload:get_active_patients"))
        self.assertEqual(response.status_code, 200)
        self.assertContains('Jane Doe')
        self.assertContains('John Doe')

    def test_get_active_patients_unauthorised(self):
        """
        Check that user is redirected to login view when trying to attempt this view when
        logged out
        """
        response = self.client.get(reverse("edcaseload:get_active_patients"))
        self.assertRedirects(response, reverse("edcaseload:login"))


class ReferPatientViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

    def test_refer_patient_get(self):
        """
        Tests that on get request the refer template is being rendered
        """
        response = self.client.get(reverse('edcaseload:refer'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edcaseload/refer.html")

    def test_refer_patient_post(self):
        """
        Tests that on correct post request a new patient is created 
        """
        response = self.client.post(reverse('edcaseload:refer'), {
            'first': 'New',
            'last': 'Patient',
            'mrn': '789012',
            'borough': 'Manhattan',
            'doa': "2000-01-27",
            'location': 'Hospital C'
        })
        self.assertRedirects(response, reverse(
            "edcaseload:get_active_patients"))
        self.assertTrue(Patient.objects.filter(mrn='789012').exists())


class DischargePatientViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # Create a patient for testing
        self.patient1 = Patient.objects.create(
            first_name='John',
            last_name='Doe',
            mrn='123456',
            borough='Brooklyn',
            doa=timezone.now(),
            dor=timezone.now(),
            location='Hospital A',
            priority=1,
            discharged_therapies=None
        )

    def test_discharge_patient(self):
        """
        Test that a patient is discharged on a POST request
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(
            reverse("edcaseload:discharge"), {"mrn": "123456"})
        self.assertRedirects(response, reverse(
            'edcaseload:get_active_patients'))
        self.patient1.refresh_from_db()
        self.assertIsNotNone(self.patient1.discharged_therapies)


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

    def test_login_get(self):
        """
        Test that the login page is rendered on GET request
        """
        response = self.client.get(reverse('edcaseload:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edcaseload/login.html')

    def test_login_post(self):
        """
        Test that a user is authenticated and redirected on POST request
        """
        response = self.client.post(reverse('edcaseload:login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertRedirects(response, reverse(
            'edcaseload:get_active_patients'))


class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_get(self):
        """
        Test that the registration page is rendered on GET request
        """
        response = self.client.get(reverse('edcaseload:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edcaseload/register.html')

    def test_register_post(self):
        """
        Test that a new user is created and authenticated on POST request
        """
        response = self.client.post(reverse('edcaseload:register'), {
            'username': 'newuser',
            'password': 'newpassword',
            'repeat_password': 'newpassword',
            'email': 'newuser@example.com'
        })
        self.assertRedirects(response, reverse(
            'edcaseload:get_active_patients'))
        self.assertTrue(User.objects.filter(username='newuser').exists())


class UpdatePatientViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # Create a patient for testing
        self.patient1 = Patient.objects.create(
            first_name='John',
            last_name='Doe',
            mrn='123456',
            borough='Brooklyn',
            doa=timezone.now(),
            dor=timezone.now(),
            location='Hospital A',
            priority=1,
            discharged_therapies=None
        )

    def test_update_patient_get(self):
        """
        Test that the update form is rendered on GET request
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(
            reverse('edcaseload:update', args=['123456']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edcaseload/update.html')

    def test_update_patient_post(self):
        """
        Test that a patient's details are updated on POST request
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('edcaseload:update', args=['123456']), {
            'mrn': '123456',
            'first': 'Updated',
            'last': 'Patient',
            'borough': 'Bronx',
            'location': 'Hospital D',
            'priority': 2,
            'contact_time': '1000'
        })
        self.assertRedirects(response, reverse(
            'edcaseload:get_active_patients'))
        self.patient1.refresh_from_db()
        self.assertEqual(self.patient1.first_name, 'Updated')


class LogoutViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

    def test_logout(self):
        """ 
        Test that the user is logged out and redirected to the login page
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('edcaseload:logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edcaseload/login.html')
