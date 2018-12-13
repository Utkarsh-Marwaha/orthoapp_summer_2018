from django import forms
from functionality.models import StepCounter, KneeMotionRange, PainLevel

class StepCounterForm(forms.ModelForm):

    class Meta():
        model  = StepCounter
        fields = ('steps',)

class KneeMotionRangeForm(forms.ModelForm):

    class Meta():
        model  = KneeMotionRange
        fields = ('bend', 'stretch')

class PainLevelForm(forms.ModelForm):

    class Meta():
        model  = PainLevel
        fields = ('painLevel', 'isExerciseDone', 'isMedicineTaken')
