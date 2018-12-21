############################## New section here    ######################################
from django import forms
from accounts.models import MyUser, Patient, Surgeon, Operation

class UserForm(forms.ModelForm):

    password = forms.CharField(widget = forms.PasswordInput())

    class Meta():
        model = MyUser
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

class PatientProfileInfoForm(forms.ModelForm):

    class Meta():
        model = Patient
        fields = ('dateOfBirth',)

class SurgeonProfileInfoForm(forms.ModelForm):

    class Meta():
        model = Surgeon
        fields = ('hospital_name',)

class OperationInfoForm(forms.ModelForm):

    class Meta():
        model = Operation
        fields = '__all__'
