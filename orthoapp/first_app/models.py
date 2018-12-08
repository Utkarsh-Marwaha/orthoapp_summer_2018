from django.db import models
# from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from timezone_field import TimeZoneField
from django.contrib.auth.models import AbstractUser

from django.conf import settings
# Create your models here.

class MyUser(AbstractUser):
    is_patient = models.BooleanField('patient status', default=False)
    is_surgeon = models.BooleanField('surgeon status', default=False)
    is_practice = models.BooleanField('surgeon status', default=True)

class UserProfileInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    # firstName = user.first_name
    # lastName = user.last_name
    # email = user.email

    # additional characteristics
    profile_pic = models.ImageField(upload_to = 'profile_pics', blank=True)
    def __str__(self):
        return self.user.username
# #this is an abstract class named Person, It features
# #might have to change the name of Person class to User
# class Person(models.Model):
#     firstName    = models.CharField(max_length=100)
#     lastName     = models.CharField(max_length=100)
#     email        = models.EmailField(max_length=100)
#
#     class Meta:
#         abstract = True
#
#     def __str__(self):
#         return self.firstName+" "+self.lastName
# User.profile = property(lambda u: UserProfileInfo.objects.get_or_create(user=u)[0])

class Patient(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    dateOfBirth = models.DateField()
    def __str__(self):
        return self.user.username

class Surgeon(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    hospital_name = models.CharField(max_length = 264)
    patients = models.ManyToManyField(Patient, through='Operation')
    def __str__(self):
        return self.user.username

class Practice(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    hospital_name = models.CharField(max_length = 264)
    def __str__(self):
        return self.user.username

class Operation(models.Model):
    KNEE = 'K'
    HIP  = 'H'
    OPERATION_TYPE_CHOICES =(
    (KNEE, 'Knee'),
    (HIP, 'Hip'),
    )

    LEFT   = 'L'
    RIGHT  = 'R'
    BOTH   = 'B'
    OPERATION_SIDE_CHOICES =(
    (LEFT, 'Left'),
    (RIGHT, 'Right'),
    (BOTH, 'Both'),
    )

    PRIMARY = 'P'
    REVISION  = 'R'
    SURGERY_TYPE_CHOICES =(
    (PRIMARY, 'Primary'),
    (REVISION, 'Revision'),
    )

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    surgeon = models.ForeignKey(Surgeon, on_delete=models.CASCADE)

    # operationType = models.CharField(max_length = 1, choices = OPERATION_TYPE_CHOICES, default=KNEE)
    # operationSide = models.CharField(max_length = 1, choices = OPERATION_SIDE_CHOICES, default=LEFT)
    # surgeryType   = models.CharField(max_length = 1, choices = SURGERY_TYPE_CHOICES, default=PRIMARY)

    operationType = models.CharField(max_length = 1, choices = OPERATION_TYPE_CHOICES)
    operationSide = models.CharField(max_length = 1, choices = OPERATION_SIDE_CHOICES)
    surgeryType   = models.CharField(max_length = 1, choices = SURGERY_TYPE_CHOICES)

    surgeryDate = models.DateField()

    def __str__(self):
        return str(self.surgeryDate)+" "+self.surgeryType+" "+self.operationSide +" "+self.operationType

class DataPoint(models.Model):
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        abstract = True

    def __str__(self):
        return str(self.created)

class StepCounter(DataPoint):
    steps = models.IntegerField(default=0)

class KneeMotionRange(DataPoint):
    bend = models.FloatField(default=90)
    stretch = models.FloatField(default=90)


class PainLevel(DataPoint):
    painLevel = models.IntegerField(
    default=0,
    validators=[MaxValueValidator(10), MinValueValidator(0)])

    isExerciseDone = models.BooleanField()
    isMedicineTaken = models.BooleanField()

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=512)
    time = models.DateTimeField()
    time_zone = TimeZoneField(default='Australia/Sydney')
    # Additional fields not visible to users
    # The task_id field will help us keep track of the corresponding reminder task for this appointment
    task_id = models.CharField(max_length=50, blank=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.task_id + " " +self.title

#############################          STATIC SECTION        ###############################################################
class static_page(models.Model):
    name = models.CharField(max_length=25)
    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Welcome_To_Orthoapp(static_page):
    name = "Welcome To Orthoapp Page"
    introduction = models.TextField(blank=True)
    acknowledgements = models.TextField(blank=True)
    disclaimer = models.TextField(blank=True)
    copyright = models.TextField(blank=True)


class Before_Your_Surgery(static_page):
    name = "Before Surgery Information Page"
    pre_admission_process  = models.TextField(blank=True)
    medical_tests  = models.TextField(blank=True)
    preparing  = models.TextField(blank=True)
    arranging_support  = models.TextField(blank=True)
    minimising_risk_of_cancellation  = models.TextField(blank=True)
    hospital_admission  = models.TextField(blank=True)
