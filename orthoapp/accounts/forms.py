############################## New section here    ######################################
from django import forms
from accounts.models import MyUser, Patient, Surgeon, Operation

class DateInput(forms.DateInput):
    input_type = 'date'

class UserForm(forms.ModelForm):

    # password = forms.CharField(widget = forms.PasswordInput())

    class Meta():
        model = MyUser
        fields = ('username', 'email', 'first_name', 'last_name')

GENDER_CHOICES = (('0', 'Female'),('1', 'Male'),)
class PatientProfileInfoForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect())

    class Meta():
        model = Patient
        fields = ('gender','dateOfBirth',)
        widgets = {
            'dateOfBirth': DateInput(),

        }

class SurgeonProfileInfoForm(forms.ModelForm):

    class Meta():
        model = Surgeon
        fields = ('hospital_name',)

# This form is needed when we need to assign a new Operation to an existing patient
class OperationInfoForm(forms.ModelForm):

    class Meta():
        model = Operation
        fields = '__all__'
        widgets = {
            'surgeryDate': DateInput(),

        }


# This form is created to be displayed while creating record of a new patient
class PatientOperationInfoForm(forms.ModelForm):

    class Meta():
        model = Operation
        exclude = ('patient',)
        widgets = {
            'surgeryDate': DateInput(),
        }
