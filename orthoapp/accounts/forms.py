############################## New section here    ######################################
from django import forms
from accounts.models import MyUser, Patient, Surgeon, Operation
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget, PhoneNumberInternationalFallbackWidget

class DateInput(forms.DateInput):
    input_type = 'date'

class UserForm(forms.ModelForm):

    # to set mandatory fields
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta():
        model = MyUser
        fields = ('username', 'email', 'first_name', 'last_name')

GENDER_CHOICES = (('0', 'Female'),('1', 'Male'),)
class PatientProfileInfoForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect())
    # uncomment the following line to add phone number and added the "phoneNumber" to the tuple of fields
    # phoneNumber=PhoneNumberField(widget=PhoneNumberPrefixWidget())
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
