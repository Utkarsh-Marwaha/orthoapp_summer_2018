from first_app.models import Welcome_To_Orthoapp, Before_Your_Surgery
from django.shortcuts import render, redirect
from first_app.forms import SurgeonProfileInfoForm, PatientProfileInfoForm, UserForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required # login decorator that makes it easier
from first_app.decorators import patient_required, surgeon_required, practice_required
# Create your views here.
def index(request):
    if request.user.is_authenticated:
        if request.user.is_surgeon:
            return render(request, 'first_app/surgeon.html')
        else:
            return render(request, 'first_app/patient.html')
    return render(request, 'first_app/index.html', {})

def welcome_to_orthoapp(request):
    lis = Welcome_To_Orthoapp.objects.all()
    welcome_to_ortho_page = {'welcome_to_ortho_page': lis}
    return render(request, 'first_app/welcome_to_orthoapp.html', context = welcome_to_ortho_page)

def before_your_surgery(request):
    lis = Before_Your_Surgery.objects.all()
    before_your_surgery_page = {'before_your_surgery_page': lis}
    return render(request, 'first_app/before_your_surgery.html', context = before_your_surgery_page)



@login_required
def special(request):
    # Remember to also set login url in settings.py!
    # LOGIN_URL = '/first_app/user_login/'
    return HttpResponse("You are logged in. Nice!")

# Note here that inside of our user_logout function, there is no checking if the user is logged in or not
# the beauty of django is that to do so, you just have to use the decorator login_required. AND THAT IS IT! beautiful.
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register_patient(request):

    registered = False

    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST)
        profile_form = PatientProfileInfoForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save User Form to Database
            user = user_form.save(commit=False)
            user.is_patient=True
            user.is_practice=False

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()

            # Now we deal with the extra info!

            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user

            # Check if they provided a profile picture
            if 'profile_pic' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.profile_pic = request.FILES['profile_pic']

            # Now save model
            profile.save()

            # Registration Successful!
            registered = True

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors,profile_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = PatientProfileInfoForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'first_app/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})



def register_surgeon(request):
    registered = False
    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST)
        profile_form = SurgeonProfileInfoForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save User Form to Database
            user = user_form.save(commit=False)
            user.is_surgeon=True
            user.is_practice=False

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()

            # Now we deal with the extra info!

            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user

            # Check if they provided a profile picture
            if 'profile_pic' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.profile_pic = request.FILES['profile_pic']

            # Now save model
            profile.save()

            # Registration Successful!
            registered = True

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors,profile_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = SurgeonProfileInfoForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'first_app/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username') #this get will grab it from the HTML
        password = request.POST.get('password')

        user = authenticate(username=username, password=password) #user is a boolean that tells us if it is authenticated or not
        if user:
            print("HAHAHHAHAHAHA")
            print(user.is_patient)
            print("HEHEHEHEHEHEHEHE")
            # if user.is_active and user.is_patient:
            if user.is_active and (user.is_surgeon or user.is_patient):
                login(request, user)
                # return HttpResponseRedirect(reverse('index')) #if its everything ok with the login and password, you will log in and be redirected to the index page
                return redirect('first_app:index')
            else:
                return HttpResponse("ACCESS DENIED!")
        else:
            print("LOGIN FAILED!")
            print("Username: {} and password {}".format(username, password))
            return HttpResponse("Invalid login details supplied!")
    else:
        return render(request,'first_app/login.html',{})

# @login_required
# @patient_required
# def patient_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username') #this get will grab it from the HTML
#         password = request.POST.get('password')
#
#         user = authenticate(username=username, password=password) #user is a boolean that tells us if it is authenticated or not
#         if user:
#             print("HAHAHHAHAHAHA")
#             print(user.is_patient)
#             print("HEHEHEHEHEHEHEHE")
#             # if user.is_active and user.is_patient:
#             if user.is_active and user.is_patient:
#                 login(request, user)
#                 # return HttpResponseRedirect(reverse('index')) #if its everything ok with the login and password, you will log in and be redirected to the index page
#                 return render(request,'first_app/patient.html',{})
#             else:
#                 return HttpResponse("ACCESS DENIED!")
#         else:
#             print("LOGIN FAILED!")
#             print("Username: {} and password {}".format(username, password))
#             return HttpResponse("Invalid login details supplied!")
#     else:
#         return render(request,'first_app/login.html',{})
#
# def surgeon_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username') #this get will grab it from the HTML
#         password = request.POST.get('password')
#
#         user = authenticate(username=username, password=password) #user is a boolean that tells us if it is authenticated or not
#         if user:
#             print("HAHAHHAHAHAHA")
#             print(user.is_surgeon)
#             print("HEHEHEHEHEHEHEHE")
#             # if user.is_active and user.is_patient:
#             if user.is_active and user.is_surgeon:
#                 login(request, user)
#                 # return HttpResponseRedirect(reverse('index')) #if its everything ok with the login and password, you will log in and be redirected to the index page
#                 return render(request,'first_app/surgeon.html',{})
#             else:
#                 return HttpResponse("ACCESS DENIED!")
#         else:
#             print("LOGIN FAILED!")
#             print("Username: {} and password {}".format(username, password))
#             return HttpResponse("Invalid login details supplied!")
#     else:
#         return render(request,'first_app/login.html',{})


def practice_login(request):
    if request.method == 'POST':
        username = request.POST.get('username') #this get will grab it from the HTML
        password = request.POST.get('password')

        user = authenticate(username=username, password=password) #user is a boolean that tells us if it is authenticated or not
        if user:
            print("HAHAHHAHAHAHA")
            print(user.is_practice)
            print("HEHEHEHEHEHEHEHE")
            # if user.is_active and user.is_patient:
            if user.is_active and user.is_practice:
                login(request, user)
                # return HttpResponseRedirect(reverse('index')) #if its everything ok with the login and password, you will log in and be redirected to the index page
                return render(request,'first_app/signup.html',{})
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE!")
        else:
            print("LOGIN FAILED!")
            print("Username: {} and password {}".format(username, password))
            return HttpResponse("Invalid login details supplied!")
    else:
        return render(request,'first_app/login.html',{})


# # @login_required
# def register(request):
#
#     registered = False
#
#     if request.method == 'POST':
#
#         # Get info from "both" forms
#         # It appears as one form to the user on the .html page
#         user_form = UserForm(data=request.POST)
#         profile_form = UserProfileInfoForm(data=request.POST)
#
#         # Check to see both forms are valid
#         if user_form.is_valid() and profile_form.is_valid():
#
#             # Save User Form to Database
#             user = user_form.save()
#
#             # Hash the password
#             user.set_password(user.password)
#
#             # Update with Hashed password
#             user.save()
#
#             # Now we deal with the extra info!
#
#             # Can't commit yet because we still need to manipulate
#             profile = profile_form.save(commit=False)
#
#             # Set One to One relationship between
#             # UserForm and UserProfileInfoForm
#             profile.user = user
#             profile.is_patient = True
#             # Check if they provided a profile picture
#             if 'profile_pic' in request.FILES:
#                 print('found it')
#                 # If yes, then grab it from the POST form reply
#                 profile.profile_pic = request.FILES['profile_pic']
#
#             # Now save model
#             profile.save()
#
#             # Registration Successful!
#             registered = True
#
#         else:
#             # One of the forms was invalid if this else gets called.
#             print(user_form.errors,profile_form.errors)
#
#     else:
#         # Was not an HTTP post so we just render the forms as blank.
#         user_form = UserForm()
#         profile_form = UserProfileInfoForm()
#
#     # This is the render and context dictionary to feed
#     # back to the registration.html file page.
#     return render(request,'first_app/registration.html',
#                           {'user_form':user_form,
#                            'profile_form':profile_form,
#                            'registered':registered})
# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username') #this get will grab it from the HTML
#         password = request.POST.get('password')
#
#         user = authenticate(username=username, password=password) #user is a boolean that tells us if it is authenticated or not
#         if user:
#             print("HAHAHAHAHAHAHAHAHAHHAHAHAHAH")
#             print(user.is_patient)
#             print("HEHEHEHEHEHEHEHEHEHEHE")
#             if user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('index')) #if its everything ok with the login and password, you will log in and be redirected to the index page
#             else:
#                 print("why am i here")
#                 return HttpResponse("ACCOUNT NOT ACTIVE!")
#         else:
#             print("LOGIN FAILED!")
#             print("Username: {} and password {}".format(username, password))
#             return HttpResponse("Invalid login details supplied!")
#     else:
#         return render(request,'first_app/login.html',{})


################## new section here ############################
from django.views.generic import TemplateView

class SignUpView(TemplateView):
    template_name = 'first_app/signup.html'
