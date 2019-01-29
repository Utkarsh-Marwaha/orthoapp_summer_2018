from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

#google's phone number library
from phonenumber_field.modelfields import PhoneNumberField
#test comand 2
# Create your models here.

ORTHOPAEDICS_ACT = 'OA'
CALVARY  = 'CL'
HOSPITAL_CHOICES =(
(ORTHOPAEDICS_ACT, 'Orthopaedics ACT'),
(CALVARY, 'Calvary'),
)

class MyUser(AbstractUser):
    is_patient = models.BooleanField('patient status', default=False)
    is_surgeon = models.BooleanField('surgeon status', default=False)
    is_practice = models.BooleanField('surgeon status', default=True)

class UserProfileInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    def __str__(self):
        return self.user.username

class Patient(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    middle_name  = models.CharField(max_length = 264, null=True, blank=True)
    GENDER_CHOICES = (('0', 'Female'),('1', 'Male'),)
    gender = models.CharField(max_length=15,choices=GENDER_CHOICES, null=True, blank=False)
    dateOfBirth = models.DateField()
    phoneNumber = PhoneNumberField(null=True, blank=True, unique=True)
    def __str__(self):
        return self.user.username


class Surgeon(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    hospital_name = models.CharField(max_length = 20, choices = HOSPITAL_CHOICES, blank=False)
    patients = models.ManyToManyField(Patient, through='Operation')
    def __str__(self):
        return self.user.username

class Practice(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    hospital_name = models.CharField(max_length = 264)
    def __str__(self):
        return self.user.username

class Operation(models.Model):
    KNEE = 'Knee'
    HIP  = 'Hip'
    OPERATION_TYPE_CHOICES =(
    (KNEE, 'Knee'),
    (HIP, 'Hip'),
    )

    LEFT   = 'Left'
    RIGHT  = 'Right'
    BOTH   = 'Both'
    OPERATION_SIDE_CHOICES =(
    (LEFT, 'Left'),
    (RIGHT, 'Right'),
    (BOTH, 'Both'),
    )

    PRIMARY = 'Pri'
    REVISION  = 'Rev'
    SURGERY_TYPE_CHOICES =(
    (PRIMARY, 'Primary'),
    (REVISION, 'Revision'),
    )

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    surgeon = models.ForeignKey(Surgeon, on_delete=models.CASCADE)
    operationType = models.CharField(max_length = 5, choices = OPERATION_TYPE_CHOICES)
    operationSide = models.CharField(max_length = 5, choices = OPERATION_SIDE_CHOICES)
    surgeryType   = models.CharField(max_length = 5, choices = SURGERY_TYPE_CHOICES)

    surgeryDate = models.DateField()

    def __str__(self):
        return str(self.surgeryDate)+" "+self.surgeryType+" "+self.operationSide +" "+self.operationType
