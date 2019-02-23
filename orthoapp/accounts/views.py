from django.shortcuts import render, redirect
from accounts.forms import SurgeonProfileInfoForm, PatientProfileInfoForm, UserForm, OperationInfoForm, PatientOperationInfoForm
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required 
from accounts.decorators import patient_required, surgeon_required, practice_required
from accounts.models import MyUser
from django.core.mail import send_mail
from accounts.models import Operation
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

""" 
This function helps us to filter and differenciate the type of users after
their credentials have been succesfully authenticated    
"""
def filter_user(request):

    # check if the user has been authenticated
    if request.user.is_authenticated:
        
        # redirect to the surgeon dashboard if the user is a surgeon
        if request.user.is_surgeon:
            messages.success(request, 'You are now logged in')
            return redirect('surgeon')
    
        # redirect to the patient dashboard if the user is a patient
        elif request.user.is_patient:
            messages.success(request, 'You are now logged in')
            return redirect('patient')

        # redirect to the practice dashboard if the user is a practice
        else:
            messages.success(request, 'You are now logged in')
            return redirect('practice')

    # keep showing the home page until the user is authenticated
    return render(request, 'pages/index.html', {})

""" This function helps the user to log-out of the application """
@login_required
def user_logout(request):

    # if the logout request has been made by the user
    if request.method == 'POST':
        
        # logout the user 
        logout(request)

        # display success message on the home page
        messages.success(request, 'You are now logged out')
        return redirect('index')

""" This function helps a user with practice account to register a patient in the system """
@login_required
@practice_required
def register_patient(request):

    if request.method == 'POST':
        
        # Grab hold of information from all the forms needed to register a new patient
        user_form       = UserForm(data=request.POST)
        profile_form    = PatientProfileInfoForm(data=request.POST)
        operation_form  = PatientOperationInfoForm(data=request.POST)

        # Check if all the three different forms have been filled up correctly by the practice user
        if user_form.is_valid() and profile_form.is_valid() and operation_form.is_valid():

            ## PERSONAL DETAILS OF THE USER

            # Save User's personal details in the Database at the backend
            user = user_form.save(commit=False)

            # Set the is_patient flag as True to ensure that the register user will have access rights of patient
            user.is_patient   = True
            user.is_practice  = False
            user.is_surgeon   = False

            # create a random password for the patient
            password = MyUser.objects.make_random_password()
            # Associate the random password to the patient's account (Hash it simulataneously)
            user.set_password(password)

            # Save the user instance to the Database in the backend
            user.save()

            ## SPECIFIC DETAILS OF THE PATIENT

            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user

            # Check if they provided a profile picture
            if 'profile_pic' in request.FILES:
                
                # If yes, then grab it from the POST form reply
                profile.profile_pic = request.FILES['profile_pic']

            # Now save model
            #this profile is a patient instance
            profile.save()

            ## OPERATION DETAILS OF THE PATIENT

            operation = operation_form.save(commit=False)

            # assign the patient profile to the patient attribute of the operation instance
            operation.patient = profile

            # Save the operation instance to the Database in the backend
            operation.save()

            # set the email subject, sender's address and reciever's address
            subject, from_email, to = 'Welcome to orthoapp', 'orthoapp.feedback@gmail.com', profile.user.email
            
            # fetch the email template
            t = get_template('email/welcome.html')
            
            # create the context to be passed over to the email template
            c = {'username':  profile.user.username, 'password': password}
            
            # create the message to be sent
            msg = EmailMultiAlternatives(subject, t.render(c), from_email, [to])
            msg.attach_alternative(t.render(c), "text/html")
            
            # send the email to the patient
            msg.send()
            
            messages.success(request, 'Patient Created')
            return redirect('signup_patient')

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors,profile_form.errors,operation_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as empty forms.
        user_form       = UserForm()
        profile_form    = PatientProfileInfoForm()
        operation_form  = PatientOperationInfoForm()

    # render the registration.html template with proper context
    return render(request,'accounts/registration.html',
                          {'user_form'      : user_form,
                           'profile_form'   : profile_form,
                           'operation_form' : operation_form,
                           })

""" This function helps a user with practice account to register a surgeon in the system """
@login_required
@practice_required
def register_surgeon(request):
    
    if request.method == 'POST':

        # Grab hold of information from all the forms needed to register a new surgeon
        user_form    = UserForm(data=request.POST)
        profile_form = SurgeonProfileInfoForm(data=request.POST)

        # Check if all the forms have been filled up correctly by the practice user
        if user_form.is_valid() and profile_form.is_valid():

            ## PERSONAL DETAILS OF THE USER

            # Save User's personal details in the Database at the backend
            user = user_form.save(commit=False)

            # Set the is_surgeon flag as True to ensure that the register user will have access rights of surgeon
            user.is_surgeon  = True
            user.is_practice = False
            user.is_patient  = False

            # create a random password for the surgeon
            password = MyUser.objects.make_random_password()
            # Associate the random password to the surgeon's account (Hash it simulataneously)            
            user.set_password(password)

            # Save the user instance to the Database in the backend
            user.save()

            ## SPECIFIC DETAILS OF THE SURGEON

            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user

            # Check if they provided a profile picture
            if 'profile_pic' in request.FILES:
                
                # If yes, then grab it from the POST form reply
                profile.profile_pic = request.FILES['profile_pic']

            # Now save model
            #this profile is a surgeon instance
            profile.save()

            # set the email subject, sender's address and reciever's address
            subject, from_email, to = 'Welcome to orthoapp', 'orthoapp.feedback@gmail.com', profile.user.email
            
            # fetch the email template
            t = get_template('email/welcome.html')
            
            # create the context to be passed over to the email template
            c = {'username':  profile.user.username, 'password': password}
            
            # create the message to be sent
            msg = EmailMultiAlternatives(subject, t.render(c), from_email, [to])
            msg.attach_alternative(t.render(c), "text/html")
            
            # send the email to the surgeon
            msg.send()

            messages.success(request, 'Surgeon Created')
            return redirect('signup_surgeon')

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors,profile_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as empty forms.        
        user_form    = UserForm()
        profile_form = SurgeonProfileInfoForm()

    # This is the render and context dictionary to feed back to the registration.html file page.
    return render(request,'accounts/registration.html',
                          {'user_form'    : user_form,
                           'profile_form' : profile_form,
                           })

""" This function helps a user with practice account to assign a new operation to an existing patient """
@login_required
@practice_required
def register_operation(request):

    if request.method == 'POST':

        # Grab hold of information from the form needed to create a new operation
        operation_form = OperationInfoForm(data=request.POST)

        # Check if the form has been filled up correctly by the practice user        
        if operation_form.is_valid():

            # Save the surgical procedure's details in the Database at the backend            
            operation = operation_form.save(commit=False)

            # Save the operation instance to the Database in the backend            
            operation.save()

            messages.success(request, 'Operation Created')
            return redirect('register_operation')

        else:
            # One of the forms was invalid if this else gets called.
            print(operation_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as empty forms.
        operation_form = OperationInfoForm()

    # This is the render and context dictionary to feed back to the operation.html file page.
    return render(request,'accounts/operation.html',
                          {'operation_form':operation_form,
                           })

""" This function assists a user with a valid account to login to the system """
def user_login(request):
    if request.method == 'POST':
        
        # Grab hold of the username and password needed to login a valid user to the system
        username = request.POST.get('username')
        password = request.POST.get('password')

        # use the user credentials to authenticate the login-request
        # Note: user is a boolean variable that indicates whether or not the user was successfully authenticated 
        user = authenticate(username=username, password=password)

        # If the user credentials are valid
        if user:

            if user.is_active and (user.is_surgeon or user.is_patient or user.is_practice):
                
                # built-in django method used to login the user
                login(request, user)
                
                # redirected to filter_user function so that we can differenciate and identify the correct account type 
                return redirect('filter_user')

            else:
                # should reach here is the user is inactive or belongs to fourth user type (other than patient, surgeon and practice)
                return HttpResponse("ACCESS DENIED!")
        else:
            messages.error(request, 'Invalid login details supplied!')
            return render(request, 'accounts/login.html',{})
    else:
        # Was not an HTTP post so we just render the forms as empty forms.
        return render(request, 'accounts/login.html',{})

""" This function renders the patient dashboard """
@login_required
@patient_required
def patient(request):
    return render(request, 'accounts/patient.html')

""" This function renders the surgeon dashboard """
@login_required
@surgeon_required
def surgeon(request):

    # Grab the username of the user who initiated the request
    login_username = request.user.username

    # Fetch a list of all Operation instances
    all_operation_list = Operation.objects.all()

    #this list shall contain all the operation instances belonging to the current user
    operation_list = list()

    # cycle through all the operations
    for i in all_operation_list:
        # if surgeon name matches with login user name
        if i.surgeon.user.username == login_username:
            # then collect the corresponding operation
            operation_list.append(i)

    # index is required to display serial ID on surgeon dashboard
    index=1

    # patient_set is required because we want only unique entries
    patient_set  = set()
    patient_list = list()

    # grab all patients from list of chosen operation instances
    for j in operation_list:
        patient_set.add(j.patient)

    for k in patient_set:
        patient_list.append((k, index))
        index=index+1

    # This is the render and context dictionary to feed back to the surgeon.html file page.
    return render(request, 'accounts/surgeon.html',
                            {'operation_list': operation_list,
                             'patient_set'   : patient_list,
                            })

""" This function renders the practice dashboard """
@login_required
@practice_required
def practice(request):

    return render(request, 'accounts/signup.html', {},)


from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

""" This function assists the user to edit the password of their account """
@login_required
def change_password(request):

    if request.method == 'POST':   

        # Grab the information needed to edit/update the password
        change_password_form = PasswordChangeForm(request.user, request.POST)
        
        # Check if all the information has been correctly filled up by the user
        if change_password_form.is_valid():

            # Save the changes in the database at the backend     
            user = change_password_form.save()

            # update the current session's authentication key
            update_session_auth_hash(request, user)  # Important!
            
            # display success message
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            # Display form errors if the user has not filled it up correctly
            messages.error(request, 'Please correct the error below.')

    else:
        # Was not an HTTP post so we just render the form as empty form.        
        change_password_form = PasswordChangeForm(request.user)
   
    return render(request, 'accounts/change_password.html', {
        'change_password_form': change_password_form
    })

""" This function renders the settings page to the user """
@login_required
def user_settings(request):
    return render(request, 'accounts/user_settings.html')
