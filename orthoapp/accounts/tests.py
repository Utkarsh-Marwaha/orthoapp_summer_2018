import datetime

from django.test import TestCase

# Create your tests here.
from .models import MyUser
from .models import Patient


class PatientTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.patient_creds = {'username': 'test_patient1', 'password': 'test1234567',
                             'first_name': 'Alec', 'last_name': 'Thomas', 'email': 'alecthomas@gmail.com'}
        user = MyUser.objects.create_user(**cls.patient_creds)
        user.is_patient = True
        user.is_surgeon = False
        user.is_practice = False
        user.save()
        patient = Patient(user=user,  dateOfBirth=datetime.datetime(2000, 1, 1), gender=1)
        patient.save()


class PatientLoginTestCase(PatientTestCase):
    def test_login(self):
        logged_in = self.client.login(**self.patient_creds)
        self.assertTrue(logged_in)
        self.client.logout()


class PatientTestLandingPage(PatientTestCase):
    def test_landing_page_exists(self):
        url = '/accounts/user_login/patient'
        self.client.login(**self.patient_creds)
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        self.client.logout()


class ProfilePageTestCase(PatientTestCase):

    def test_profile_page_exists(self):
        self.client.login(**self.patient_creds)
        r = self.client.get('/accounts/user_login/patient/profile')
        self.assertEqual(r.status_code, 200)
        self.client.logout()

    def test_page_contains_personal_details(self):
        self.client.login(**self.patient_creds)
        r = self.client.get('/accounts/user_login/patient/profile')
        self.assertContains(r, "First Name")
        self.assertContains(r, self.patient_creds['first_name'])
        self.assertContains(r, "Last Name")
        self.assertContains(r, self.patient_creds['last_name'])
        self.assertContains(r, "Email")
        self.assertContains(r, self.patient_creds['email'])
