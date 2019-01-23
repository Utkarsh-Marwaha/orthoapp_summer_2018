from django import forms
from functionality.models import StepCounter, KneeMotionRange, PainLevel

class StepCounterForm(forms.ModelForm):

    class Meta():
        model  = StepCounter
        fields = ('steps',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['steps'].label = "How many steps did you take today ?"
        
class KneeMotionRangeForm(forms.ModelForm):

    class Meta():
        model  = KneeMotionRange
        fields = ('bend', 'stretch')

class PainLevelForm(forms.ModelForm):

    class Meta():
        model  = PainLevel
        fields = ('painLevel', 'isExerciseDone', 'isMedicineTaken')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['painLevel'].label = "How much pain do you have now ?"
        self.fields['isExerciseDone'].label = "How many times have you done your exercises ?"
        self.fields['isMedicineTaken'].label = "Have you taken your prescribed pain medication in the last two hours ?"
    