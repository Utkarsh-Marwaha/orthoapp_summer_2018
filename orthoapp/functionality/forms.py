from django import forms
from functionality.models import StepCounter, KneeMotionRange, PainLevel

class StepCounterForm(forms.ModelForm):

    class Meta():
        # Specifying the model whose fields will be used to build the form
        model  = StepCounter

        # Specifying the fields which will be used in the form
        fields = ('steps',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Specifying the label which will get displayed on the front-end instead of the field name itself
        self.fields['steps'].label = "How many steps did you take today ?"

class KneeMotionRangeForm(forms.ModelForm):

    class Meta():
        # Specifying the model whose fields will be used to build the form
        model  = KneeMotionRange

        # Specifying the fields which will be used in the form
        fields = ('bend', 'stretch')


class PainLevelForm(forms.ModelForm):

    class Meta():
        # Specifying the model whose fields will be used to build the form
        model  = PainLevel

        # Specifying the widgets which will be used in the form fields
        widgets = {
            'isMedicineTaken': forms.RadioSelect
        }

        # Specifying the fields which will be used in the form
        fields = ('painLevel', 'isExerciseDone', 'isMedicineTaken')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Specifying the labels which will get displayed on the front-end instead of the field name itself
        self.fields['painLevel'].label        = "How much pain do you have now ?"
        self.fields['isExerciseDone'].label   = "How many times did you do your exercise yesterday ?"
        self.fields['isMedicineTaken'].label  = "Have you taken your prescribed pain medication in the last two hours ?"
