from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from timezone_field import TimeZoneField
from django.conf import settings
from accounts.models import Operation, Patient, Surgeon


class DataPoint(models.Model):
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        abstract = True

    def __str__(self):
        return str(self.created)

class StepCounter(DataPoint):
    steps = models.IntegerField(default=0, validators=[MinValueValidator(0)])

class KneeMotionRange(DataPoint):
    bend = models.FloatField(default=90)
    stretch = models.FloatField(default=90)

BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))
class PainLevel(DataPoint):
    painLevel = models.IntegerField(
    default=0,
    validators=[MaxValueValidator(10), MinValueValidator(0)])

    isExerciseDone = models.IntegerField(
    default=0,
    validators=[MinValueValidator(0)], blank=True, null=True)

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
