# from django import forms
# from django.contrib.auth.models import User
# from first_app.models import UserProfileInfo
#
#
# class UserForm(forms.ModelForm):
#
#     password = forms.CharField(widget = forms.PasswordInput())
#
#     class Meta():
#         model = User
#         fields = ('username', 'email', 'password', 'first_name', 'last_name')
#
# class UserProfileInfoForm(forms.ModelForm):
#
#     class Meta():
#         model = UserProfileInfo
#         fields = ('profile_pic',)



############################## New section here    ######################################
from django import forms
from first_app.models import MyUser, Patient, Surgeon

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


################################ second new section here ######################################
