from django.shortcuts import render, redirect
from accounts.forms import SurgeonProfileInfoForm, PatientProfileInfoForm, UserForm, OperationInfoForm, PatientOperationInfoForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required # login decorator that makes it easier
from accounts.decorators import patient_required, surgeon_required, practice_required
from accounts.models import MyUser
from django.core.mail import send_mail


# Create your views here.
def filter_user(request):
    print("YOU HAVE ENTER THE INDEX FILTER")
    if request.user.is_authenticated:
        if request.user.is_surgeon:
            return redirect('surgeon')
        elif request.user.is_patient:
            return redirect('patient')
        else:
            return redirect('practice')
    return render(request, 'pages/index.html', {})


@login_required
def special(request):
    # Remember to also set login url in settings.py!
    # LOGIN_URL = '/accounts/user_login/'
    return HttpResponse("You are logged in. Nice!")

# Note here that inside of our user_logout function, there is no checking if the user is logged in or not
# the beauty of django is that to do so, you just have to use the decorator login_required. AND THAT IS IT! beautiful.
@login_required
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect(reverse('index'))

@login_required
@practice_required
def register_patient(request):

    registered = False
    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST)
        profile_form = PatientProfileInfoForm(data=request.POST)
        operation_form = PatientOperationInfoForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid() and operation_form.is_valid():

            # Save User Form to Database
            user = user_form.save(commit=False)

            user.is_patient=True
            user.is_practice=False
            user.is_surgeon=False

            password = MyUser.objects.make_random_password()
            # Hash the password
            user.set_password(password)

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
            #this profile is a patient instance
            profile.save()

            # operation details of a patient
            operation = operation_form.save(commit=False)

            operation.patient = profile
            operation.save()

            # Registration Successful!
            registered = True

            send_mail(
                'Welcome to orthoapp',
                'Dear user please find your credentials for logging on orthoapp \n' + profile.user.username + '\n' + password,
                from_email='orthoapp.feedback@gmail.com',
                recipient_list=[profile.user.email],
                fail_silently=False
            )

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors,profile_form.errors,operation_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = PatientProfileInfoForm()
        operation_form = PatientOperationInfoForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'accounts/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'operation_form': operation_form,
                           'registered':registered})


@login_required
@practice_required
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
            user.is_patient=False

            password = MyUser.objects.make_random_password()
            # Hash the password
            user.set_password(password)

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

            send_mail(
                'Welcome to orthoapp',
                'Dear user please find your credentials for logging on orthoapp \n' + profile.user.username + '\n' + password,
                from_email='orthoapp.feedback@gmail.com',
                recipient_list=[profile.user.email],
                fail_silently=False
            )

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors,profile_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = SurgeonProfileInfoForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'accounts/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})
@login_required
@practice_required
def register_operation(request):
    registered = False
    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        operation_form = OperationInfoForm(data=request.POST)

        # Check to see both forms are valid
        if operation_form.is_valid():
            # Save User Form to Database
            operation = operation_form.save(commit=False)

            # Update with Hashed password
            operation.save()

            # Registration Successful!
            registered = True

        else:
            # One of the forms was invalid if this else gets called.
            print(operation_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        operation_form = OperationInfoForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'accounts/operation.html',
                          {'operation_form':operation_form,
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
            if user.is_active and (user.is_surgeon or user.is_patient or user.is_practice):
                login(request, user)
                # return HttpResponseRedirect(reverse('index')) #if its everything ok with the login and password, you will log in and be redirected to the index page
                return redirect('filter_user')

            else:
                return HttpResponse("ACCESS DENIED!")
        else:
            print("LOGIN FAILED!")
            print("Username: {} and password {}".format(username, password))
            return HttpResponse("Invalid login details supplied!")
    else:
        return render(request, 'accounts/login.html',{})

@login_required
@patient_required
def patient(request):
    return render(request, 'accounts/patient.html')

@login_required
@surgeon_required
def surgeon(request):
    return render(request, 'accounts/surgeon.html')

@login_required
@practice_required
def practice(request):
    return render(request, 'accounts/signup.html')
