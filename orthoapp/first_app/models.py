from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from timezone_field import TimeZoneField
# Create your models here.

#this is an abstract class named Person, It features

class Person(models.Model):
    firstName    = models.CharField(max_length=100)
    lastName     = models.CharField(max_length=100)
    email        = models.EmailField(max_length=100)

    class Meta:
        abstract = True

    def __str__(self):
        return self.firstName+" "+self.lastName

class Patient(Person):
    dateOfBirth = models.DateField()

class Surgeon(Person):
    hospital_name = models.CharField(max_length = 264)
    patients = models.ManyToManyField(Patient, through='Operation')

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
class Welcome_To_Orthoapp(models.Model):
    introduction = models.TextField(blank=True)
    acknowledgements = models.TextField(blank=True)
    disclaimer = models.TextField(blank=True)
    copyright = models.TextField(blank=True)
