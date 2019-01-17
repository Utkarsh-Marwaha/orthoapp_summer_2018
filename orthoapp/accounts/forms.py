############################## New section here    ######################################
from django import forms
from accounts.models import MyUser, Patient, Surgeon, Operation
from bootstrap_datepicker_plus import DatePickerInput

class UserForm(forms.ModelForm):

    # password = forms.CharField(widget = forms.PasswordInput())

    class Meta():
        model = MyUser
        fields = ('username', 'email', 'first_name', 'last_name')

class PatientProfileInfoForm(forms.ModelForm):

    class Meta():
        model = Patient
        fields = ('dateOfBirth',)
        widgets = {
            'dateOfBirth': DatePickerInput(
                options={
                    "format": "YYYY-MM-DD", # moment date-time format
                    "showClose": True,
                    "showClear": True,
                    "showTodayButton": True,
                }), 
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
            'surgeryDate': DatePickerInput(
                options={
                    "format": "YYYY-MM-DD", # moment date-time format
                    "showClose": True,
                    "showClear": True,
                    "showTodayButton": True,
                }), 
        }


# This form is created to be displayed while creating record of a new patient
class PatientOperationInfoForm(forms.ModelForm):

    class Meta():
        model = Operation
        exclude = ('patient',)
        widgets = {
            'surgeryDate': DatePickerInput(
                options={
                    "format": "YYYY-MM-DD", # moment date-time format
                    "showClose": True,
                    "showClear": True,
                    "showTodayButton": True,
                }), 
        }
