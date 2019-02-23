from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from timezone_field import TimeZoneField
from django.conf import settings
from accounts.models import Operation, Patient, Surgeon

""" Every DataPoint represents a health record instance """
class DataPoint(models.Model):

    # Every data point is associated to an operation instance
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE)

    # Every data point has an associated timestamp indicating the its creation
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        # Data points will be displayed and identified through their timestamps
        return str(self.created)

class StepCounter(DataPoint):
    # Every stepcounter instance is composed of the number of steps walked by the patient
    steps = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    # By default, the step count is 0 and no patient is allowed to enter a negative amount

class KneeMotionRange(DataPoint):
    # Every KneeMotionRange instance consists of the degree measure to which a patient can bend back their knee
    bend = models.FloatField(default=90)

    # Every KneeMotionRange instance consists of the degree measure to which a patient can straighten or stretch forward their knee
    stretch = models.FloatField(default=90)

# Enumerating the options for the field isMedicineTaken
BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))

class PainLevel(DataPoint):
    # Every PainLevel instance consists of the pain score within the range 0-10
    painLevel = models.IntegerField(
    default=0,
    validators=[MaxValueValidator(10), MinValueValidator(0)])

    isExerciseDone = models.IntegerField(
    default=0,
    validators=[MinValueValidator(0)], blank=True, null=True)
    # By default, the exercise count is 0 and no patient is allowed to enter a negative amount

    isMedicineTaken = models.BooleanField(choices=BOOL_CHOICES, default=False)


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
