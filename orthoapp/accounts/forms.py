from django import forms
from accounts.models import MyUser, Patient, Surgeon, Operation
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget, PhoneNumberInternationalFallbackWidget

# This class allows us to use the widget for picking the date
class DateInput(forms.DateInput):
    input_type = 'date'

class UserForm(forms.ModelForm):

    # To make the fields compulsory we set the value of the attribute named required as True
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required       = True
        self.fields['first_name'].required  = True
        self.fields['last_name'].required   = True

    class Meta():
        # Specifying the model whose fields will be used to build the form
        model  = MyUser

        # Specifying the fields which will be used in the form
        fields = ('username', 'email', 'first_name', 'last_name')

class PatientProfileInfoForm(forms.ModelForm):

    # uncomment the following line to add phone number and added the "phoneNumber" to the tuple of fields
    # phoneNumber=PhoneNumberField(widget=PhoneNumberPrefixWidget())

    class Meta():
        # Specifying the model whose fields will be used to build the form
        model   = Patient

        # Specifying the fields which will be used in the form
        fields  = ('middle_name','gender','dateOfBirth',)

        # Specifying the widgets which will be used in the form fields
        widgets = {
            'dateOfBirth': DateInput(),
            'gender': forms.RadioSelect
        }

class SurgeonProfileInfoForm(forms.ModelForm):

    class Meta():
        # Specifying the model whose fields will be used to build the form
        model = Surgeon

        # Specifying the fields which will be used in the form
        fields = ('hospital_name',)

# This form is needed when we need to assign a new Operation to an existing patient
class OperationInfoForm(forms.ModelForm):

    class Meta():
        # Specifying the model whose fields will be used to build the form
        model = Operation

        # Shorthand way of saying that we need all fields from the model to be part of the form
        fields = '__all__'

        # Specifying the widgets which will be used in the form fields
        widgets = {
            'surgeryDate': DateInput(),
        }

# This form is created to be displayed while creating record of a new patient
class PatientOperationInfoForm(forms.ModelForm):

    class Meta():
        # Specifying the model whose fields will be used to build the form
        model = Operation

        # Shorthand way of saying that we need all fields except 'patient' from the model to be part of the form
        exclude = ('patient',)
        widgets = {
            'surgeryDate': DateInput(),
        }
