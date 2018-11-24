from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator




# Create your models here.
class Person(models.Model):
    firstName    = models.CharField(max_length=100)
    lastName     = models.CharField(max_length=100)
    email        = models.EmailField(max_length=100)

    class Meta:
        abstract = True

    def __str__(self):
        return self.firstName+" "+self.lastName

class Surgeon(Person):
    hospital_name = models.CharField(max_length = 264)

class Patient(Person):

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


    surgeon = models.ForeignKey(Surgeon, on_delete=models.CASCADE, related_name="patients")
    operationType = models.CharField(max_length = 1, choices = OPERATION_TYPE_CHOICES)
    operationSide = models.CharField(max_length = 1, choices = OPERATION_SIDE_CHOICES)
    surgeryType   = models.CharField(max_length = 1, choices = SURGERY_TYPE_CHOICES)
    surgeryDate = models.DateField()
    dateOfBirth = models.DateField()




class DataPoint(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
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
