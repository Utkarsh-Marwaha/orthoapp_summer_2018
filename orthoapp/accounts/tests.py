import datetime

from django.test import TestCase
from django.urls import reverse

from .models import Surgeon, MyUser, Patient, Practice


def create_and_save_test_patient(creds):
    user = MyUser.objects.create_user(**creds)
    user.is_patient = True
    user.is_surgeon = False
    user.is_practice = False
    user.save()
    patient = Patient(user=user, dateOfBirth=datetime.datetime(2000, 1, 1), gender=1)
    patient.save()


def create_and_save_test_surgeon(creds):
    user = MyUser.objects.create_user(**creds)
    user.is_patient = False
    user.is_surgeon = True
    user.is_practice = False
    user.save()
    surgeon = Surgeon(user=user, hospital_name=1)
    surgeon.save()


def create_and_save_test_practice(creds):
    user = MyUser.objects.create_superuser(**creds)
    user.is_patient = False
    user.is_surgeon = False
    user.is_practice = True
    user.save()
    practice = Practice(user=user, hospital_name=1)
    practice.save()


class PatientTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):

        cls.patient_1_creds = {'username': 'test_patient1', 'password': 'test1234567',
                               'first_name': 'Alec', 'last_name': 'Thomas', 'email': 'alec@sdfasf.com'}
        create_and_save_test_patient(cls.patient_1_creds)

        cls.patient_2_creds = {'username': 'test_patient2', 'password': 'test1234567',
                               'first_name': 'Utkarsh', 'last_name': 'Marwaha', 'email': 'utkarsh@sadfsaf.com'}
        create_and_save_test_patient(cls.patient_2_creds)

        cls.surgeon_1_creds = {'username': 'test_surgeon1', 'password': 'test1234567', 'first_name': 'Chengwu',
                               'last_name': 'Shi', 'email': 'chengwu@asdfa.com'}
        create_and_save_test_surgeon(cls.surgeon_1_creds)

        cls.practice_1_creds = {'username': 'test_practice1', 'password': 'test1234567', 'first_name': 'Liza',
                                'last_name': 'Goncharov', 'email': 'liza@safsaf.com'}
        create_and_save_test_practice(cls.practice_1_creds)

        cls.server_name = 'domain.com'


class PatientLoginTestCase(PatientTestCase):
    def test_login(self):
        print(Patient.objects.get(pk=1))
        logged_in = self.client.login(**self.patient_1_creds)
        self.assertTrue(logged_in)
        self.client.logout()


class PatientTestLandingPage(PatientTestCase):
    def test_landing_page_exists(self):
        url = '/accounts/user_login/patient'
        self.client.login(**self.patient_1_creds)
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        self.client.logout()


class ProfilePageTestCase(PatientTestCase):

    def test_profile_page_exists(self):
        self.client.login(**self.patient_1_creds)
        r = self.client.get('/accounts/user_login/patient/profile')
        self.assertEqual(r.status_code, 200)
        self.client.logout()

    def test_page_contains_personal_details(self):
        self.client.login(**self.patient_1_creds)
        r = self.client.get('/accounts/user_login/patient/profile')
        self.assertContains(r, "First Name")
        self.assertContains(r, self.patient_1_creds['first_name'])
        self.assertContains(r, "Last Name")
        self.assertContains(r, self.patient_1_creds['last_name'])
        self.assertContains(r, "Email")
        self.assertContains(r, self.patient_1_creds['email'])

    def test_that_if_user_is_not_logged_in_they_cannot_see_a_patients_details(self):
        self.client.login(**self.patient_1_creds)
        self.client.logout()
        r = self.client.get('/accounts/user_login/patient/profile', follow=True)
        self.assertNotContains(r, self.patient_1_creds['first_name'], 404)
        self.assertNotContains(r, self.patient_1_creds['last_name'], 404)
        self.assertNotContains(r, self.patient_1_creds['email'], 404)

    def test_patient_cannot_see_other_patients_details(self):
        self.client.login(**self.patient_1_creds)
        self.client.logout()
        self.client.login(**self.patient_2_creds)
        r = self.client.get('/accounts/user_login/patient/profile')
        self.assertNotContains(r, self.patient_1_creds['first_name'])
        self.assertNotContains(r, self.patient_1_creds['last_name'])
        self.assertNotContains(r, self.patient_1_creds['email'])
        self.client.logout()

    def test_surgeon_cannot_see_a_patients_details(self):
        self.client.login(**self.patient_1_creds)
        self.client.logout()
        self.client.login(**self.surgeon_1_creds)
        r = self.client.get('/accounts/user_login/patient/profile')
        self.assertNotEqual(r.status_code, 200)
        self.assertNotContains(r, self.patient_1_creds['first_name'], r.status_code)
        self.assertNotContains(r, self.patient_1_creds['last_name'], r.status_code)
        self.assertNotContains(r, self.patient_1_creds['email'], r.status_code)
        self.client.logout()

    def test_practice_cannot_see_a_patients_details(self):
        self.client.login(**self.patient_1_creds)
        self.client.logout()
        self.client.login(**self.practice_1_creds)
        r = self.client.get('/accounts/user_login/patient/profile')
        self.assertNotEqual(r.status_code, 200)
        self.assertNotContains(r, self.patient_1_creds['first_name'], r.status_code)
        self.assertNotContains(r, self.patient_1_creds['last_name'], r.status_code)
        self.assertNotContains(r, self.patient_1_creds['email'], r.status_code)
        self.client.logout()

    def test_there_is_link_from_dashboard_to_profile_page(self):
        self.client.login(**self.patient_1_creds)
        r = self.client.get('/accounts/user_login/patient/', SERVER_NAME=self.server_name)
        self.assertContains(r, "<a href=\"{}{}\">".format(self.server_name, reverse('patient_profile')))

    def test_there_is_a_link_to_operation_on_profile_page(self):
        self.client.login(**self.patient_1_creds)
        r = self.client.get('/accounts/user_login/patient/profile', SERVER_NAME=self.server_name)
        self.assertContains(r, "<a href=\"{}{}\">".format(self.server_name, reverse('patient_operations')))
