from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

#google's phone number library
from phonenumber_field.modelfields import PhoneNumberField

# Enumerating the options for the field hospital_name
ORTHOPAEDICS_ACT = 'OA'
CALVARY  = 'CL'
HOSPITAL_CHOICES =(
(ORTHOPAEDICS_ACT, 'Orthopaedics ACT'),
(CALVARY, 'Calvary'),
)

""" If the users on your application can assume multiple roles at the same time (e.g. be a Patient and Surgeon),
    or your application will have only a few user types, you can control that information in the central User model
    and create flags like is_patient and is_surgeon: """
class MyUser(AbstractUser):
    is_patient  = models.BooleanField('patient status',  default=False)
    is_surgeon  = models.BooleanField('surgeon status',  default=False)
    is_practice = models.BooleanField('surgeon status',  default=True)

# This is the common information that is shared by the different kinds of users in our app.
class UserProfileInfo(models.Model):

    # Authentication in our app happens through custom user instead of the default django user
    user        = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    
    # Users will be displayed and identified through their username
    def __str__(self):
        return self.user.username

# This information is specific only to those users who are identified as Patients.
class Patient(models.Model):

    # Authentication in our app happens through custom user instead of the default django user
    user         = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    # middle name of the patient is an optional text field
    middle_name  = models.CharField(max_length = 264, null=True, blank=True)

    # the gender of the patient can be set as one of the following four options
    GENDER_CHOICES = (('0', 'Female'),('1', 'Male'),('2', 'Other'),('3', 'Rather not say'),)
    gender = models.CharField(max_length=15,choices=GENDER_CHOICES, default='3', blank=False)

    # date of birth of the patient
    dateOfBirth = models.DateField()

    # phone number of the patient is an optional field
    phoneNumber = PhoneNumberField(null=True, blank=True, unique=True)

    # Patient Users will be displayed and identified through their username
    def __str__(self):
        return self.user.username

# This information is specific only to those users who are identified as Surgeons.
class Surgeon(models.Model):

    # Authentication in our app happens through custom user instead of the default django user
    user          = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    # the hospital name of the surgeon can be set as one of the options mentioned in HOSPITAL_CHOICES
    hospital_name = models.CharField(max_length = 20, choices = HOSPITAL_CHOICES, blank=False)
    
    # This establishes a many to many relationship between surgeons and patients through an associative class named Operation
    patients      = models.ManyToManyField(Patient, through='Operation')

    # Surgeon Users will be displayed and identified through their username
    def __str__(self):
        return self.user.username

# This information is specific only to those users who are identified as Practice.
class Practice(models.Model):

    # Authentication in our app happens through custom user instead of the default django user
    user          = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    hospital_name = models.CharField(max_length = 264)

    # Surgeon Users will be displayed and identified through their username
    def __str__(self):
        return self.user.username

class Operation(models.Model):

    # Enumerating the options for the field operationType
    KNEE = 'Knee'
    HIP  = 'Hip'
    OPERATION_TYPE_CHOICES =(
    (KNEE, 'Knee'),
    (HIP, 'Hip'),
    )

    # Enumerating the options for the field operationSide
    LEFT   = 'Left'
    RIGHT  = 'Right'
    BOTH   = 'Both'
    OPERATION_SIDE_CHOICES =(
    (LEFT, 'Left'),
    (RIGHT, 'Right'),
    (BOTH, 'Both'),
    )

    # Enumerating the options for the field surgeryType
    PRIMARY = 'Pri'
    REVISION  = 'Rev'
    SURGERY_TYPE_CHOICES =(
    (PRIMARY, 'Primary'),
    (REVISION, 'Revision'),
    )

    # Each operation instance consists of one and only one patient
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    # Each operation instance consists of one and only one surgeon
    surgeon = models.ForeignKey(Surgeon, on_delete=models.CASCADE)

    # Each operation instance consists surgical details like OPERATION_TYPE_CHOICES (knee or hip)
    operationType = models.CharField(max_length = 5, choices = OPERATION_TYPE_CHOICES)

    # Each operation instance consists surgical details like OPERATION_SIDE_CHOICES (left, right or both)    
    operationSide = models.CharField(max_length = 5, choices = OPERATION_SIDE_CHOICES)

    # Each operation instance consists surgical details like SURGERY_TYPE_CHOICES (primary or revision)    
    surgeryType   = models.CharField(max_length = 5, choices = SURGERY_TYPE_CHOICES)

    # Each operation instance mentions the surgery date
    surgeryDate = models.DateField()

    # Operation instances will be displayed in the following format <surgeryDate surgeryType operationSide operationType>
    def __str__(self):
        return str(self.surgeryDate)+" "+self.surgeryType+" "+self.operationSide +" "+self.operationType
