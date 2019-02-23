from django.shortcuts import render, redirect
from functionality.forms import StepCounterForm, KneeMotionRangeForm, PainLevelForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required # login decorator that makes it easier
from accounts.decorators import patient_required, surgeon_required, practice_required
from accounts.models import Operation

from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages
import datetime



"""This function is used to render the stepcounter page using which the patient can enter their stepcounts (health data)"""
@login_required
@patient_required
def stepcounter(request):
    
    # Grab the username of the user who initiated the request
    login_username = request.user.username

    # Fetch a list of all Operation instances
    all_operation_list = Operation.objects.all()
    
    #this list shall contain all the operation instances belonging to the current user    
    operation_list = list()

    # cycle through all the operations
    for i in all_operation_list:
        # if patient username matches with login user name
        if i.patient.user.username == login_username:
            # then collect the corresponding operation
            operation_list.append(i)

    if request.method == 'POST':

        try:
            # Grab the operation selected by the patient
            selected_operation = request.POST['selected_operation']
        except MultiValueDictKeyError:
            # Display error message if the patient didn't select any operation
            messages.error(request, 'Please Select an Operation')
            return redirect('stepcounter')

        # Grab the form which contains information about the step count entered by the patient
        stepcounter_form = StepCounterForm(data=request.POST)

        # Check if the form was correctly filled up by the patient
        if stepcounter_form.is_valid():
            step_counter_object = stepcounter_form.save(commit=False)

            # cycle through all the operations associated with the current patient   
            for j in operation_list:
                # if the selected operation is found
                if str(j) == selected_operation:
                    # assign the step counter record to that operation
                    step_counter_object.operation = j

            # save the step counter instance
            step_counter_object.save()

            # Display success message after the data has been successfully saved in the database at the backend
            messages.success(request, 'Data saved ')
            return redirect('stepcounter')

        else:
            # Display an error message if the patient did not fill up the form correctly
            messages.error(request, 'Invalid Data entered')
            return redirect('stepcounter')
    else:
        # Was not an HTTP post so we just render the form as empty form.                
        stepcounter_form = StepCounterForm()

    # render the stepcounter.html file and pass on the context dictionary    
    return render(request, 'functionality/stepcounter.html',{
        'stepcounter_form' : stepcounter_form,
        'operation_list'   : operation_list
    })


"""This function is used to render the kneemotionrange page using which the patient can enter their kneemotion range (health data)"""
@login_required
@patient_required
def kneemotionrange(request):
    
    # Grab the username of the user who initiated the request
    login_username = request.user.username

    # Fetch a list of all Operation instances    
    all_operation_list = Operation.objects.all()

    # This list shall contain all the operation instances belonging to the current user        
    operation_list = list()

    # cycle through all the operations
    for i in all_operation_list:
        # if patient username matches with login user name
        if i.patient.user.username == login_username:
            # then collect the corresponding operation
            operation_list.append(i)

    if request.method == 'POST':

        try:
            # Grab the operation selected by the patient
            selected_operation = request.POST['selected_operation']
        except MultiValueDictKeyError:
            # Display error message if the patient didn't select any operation
            messages.error(request, 'Please Select an Operation')
            return redirect('kneemotionrange')

        # Grab the form which contains information about the knee motion range entered by the patient        
        kneemotionrange_form = KneeMotionRangeForm(data=request.POST)
        
        # Check if the form was correctly filled up by the patient        
        if kneemotionrange_form.is_valid():
            kneemotionrange_object = kneemotionrange_form.save(commit=False)

            # cycle through all the operations associated with the current patient
            for j in operation_list:
                # if the selected operation is found
                if str(j) == selected_operation:
                    # assign the knee motion range record to that operation
                    kneemotionrange_object.operation = j

            kneemotionrange_object.bend     = float(request.POST['bend'])
            kneemotionrange_object.stretch  = float(request.POST['stretch'])

            # save the knee motion range instance
            kneemotionrange_object.save()
            
            # Display success message after the data has been successfully saved in the database at the backend
            messages.success(request, 'Data saved ')
            return redirect('kneemotionrange')

        else:
            # Display an error message if the patient did not fill up the form correctly
            messages.error(request, 'Invalid Data entered')
            return redirect('kneemotionrange')
    else:
        # Was not an HTTP post so we just render the form as empty form.                
        kneemotionrange_form = KneeMotionRangeForm()

    # render the kneemotionrange.html file and pass on the context dictionary    
    return render(request, 'functionality/kneemotionrange.html',{
        'operation_list'   : operation_list
    })

# This is just an integer value assigned to the custom message in django
PAIN_ALERT = 50
"""This function is used to render the painlevel page using which the patient can enter their pain level range (health data)"""
@login_required
@patient_required
def painlevel(request):
    
    # Grab the username of the user who initiated the request
    login_username = request.user.username

    # Fetch a list of all Operation instances    
    all_operation_list = Operation.objects.all()

    # This list shall contain all the operation instances belonging to the current user        
    operation_list = list()

    # cycle through all the operations
    for i in all_operation_list:
        # if patient username matches with login user name
        if i.patient.user.username == login_username:
            # then collect the corresponding operation
            operation_list.append(i)

    if request.method == 'POST':

        try:
            # Grab the operation selected by the patient
            selected_operation = request.POST['selected_operation']
        except MultiValueDictKeyError:
            # Display error message if the patient didn't select any operation
            messages.error(request, 'Please Select an Operation')
            return redirect('painlevel')

        # Grab the form which contains information about the pain level entered by the patient        
        painlevel_form = PainLevelForm(data=request.POST)

        # Check if the form was correctly filled up by the patient        
        if painlevel_form.is_valid():
            painlevel_object = painlevel_form.save(commit=False)

            # Create a temporary instance of Operation class
            temp = Operation()

            # cycle through all the operations associated with the current patient            
            for j in operation_list:
                # if the selected operation is found
                if str(j) == selected_operation:
                # then assign the corresponding operation
                    painlevel_object.operation = j
                    temp = j

            # If the patient has just entered the first pain level record ever then there is no previous reference
            if PainLevel.objects.all().filter(operation=temp).count() == 0:
                latest_painlevel_object = None
            # if not then
            else:
                # Grab the latest record entered by the patient 
                latest_painlevel_object = PainLevel.objects.all().filter(operation=temp).latest('created')
            
            # save the pain level range instance             
            painlevel_object.save()

            ########## Check for 2 consecutive pain level scores of 7 or above within the last seven (7) hours
            if latest_painlevel_object is not None:
                
                # This reflects the pain score of the latest entry in the database
                latest_painlevel = latest_painlevel_object.painLevel
                # This reflects the time stamp of the latest entry in the database                
                latest_created   = latest_painlevel_object.created

                # This reflects the pain score of the current entry submitted by the user
                current_painlevel = painlevel_object.painLevel
                # This reflects the time stamp of the current entry submitted by the user
                current_created   = painlevel_object.created

                # This is how far back we're testing the entries for
                pain_level_hours     = 7

                # This is how much the pain threshold should for the PAIN ALERT to be considered
                pain_level_threshold = 7

                # The time difference between current entry and latest entry 
                difference = current_created - latest_created
                
                # The last two pain level scores have to be equal to or above 7 and submitted within 7 hours of each other
                if difference.days == 0 and difference.seconds <= pain_level_hours*60*60 and current_painlevel >=pain_level_threshold and latest_painlevel >=pain_level_threshold:
                    
                    # Save the data and display success message
                    messages.success(request, 'Data saved')

                    # Raise the PAIN LEVEL ALERT
                    messages.add_message(request, PAIN_ALERT,"You might like to contact your G.P about your pain")
                    
                    return redirect('painlevel')
                else:
                    # Display success message once the data is saved correctly to the database in the backend
                    messages.success(request, 'Data saved ')
                    return redirect('painlevel')
            else:
                # Display success message once the data is saved correctly to the database in the backend
                messages.success(request, 'Data saved ')
                return redirect('painlevel')

        else:
            # Display error message if the patient has not filled up the form correctly
            messages.error(request, 'Invalid Data entered')
            return redirect('painlevel')
    else:
        # Was not an HTTP post so we just render the form as empty form.                
        painlevel_form = PainLevelForm()

    # render the painlevel.html file and pass on the context dictionary    
    return render(request, 'functionality/painlevel.html',{
        'painlevel_form' : painlevel_form,
        'operation_list' : operation_list
    })

######################## new section here #########################


from accounts.models import MyUser
from django.views.generic import View
from functionality.models import StepCounter, KneeMotionRange, PainLevel



############################## ANOTHER SECTION USING HIGHCHART ###########################################
import json
from django.db.models import Count, Q
from django.core.serializers.json import DjangoJSONEncoder

""" This function fetches the health data associated to a patient from the backend and displays it 
    in the form of charts (as instructed) """
@login_required
def chart(request):

    # This variable will hold the username of the patient/surgeon who is trying to access the charts
    login_username = ""

    """ This variable will help to distinguish between POST requests coming from selecting the View records button
    on the surgeon dashboard and the filter operation button on the charts page"""
    switch=False

    if request.method == "POST":
        if 'switch' in request.POST:
            switch = request.POST["switch"]



    # The charts are not be viewed by the practice and so we just redirect them back to home page
    if request.user.is_practice:
        return render(request, 'pages/index.html', {})

    elif request.user.is_surgeon and not switch:
        if request.method == 'POST':
            login_username = request.POST["patient_user"]
            switch = True
            print("HI SURGEON")
            print(login_username)
        else:
            print("JUST HERE")
            return render(request, 'pages/index.html', {})

    else:
        # get the user name of the user who is currently logged in to the website
        if not switch:
            login_username = request.user.username
        else:

            if request.method == 'POST' and request.user.is_surgeon:

                login_username = request.POST["patient_user"]
                switch = False

    #this list contains all the operation objects
    all_operation_list = Operation.objects.all()
    #this list contains all the operation objects filtered by login_username
    operation_list = list()
    for i in all_operation_list:
        if i.patient.user.username == login_username:
            operation_list.append(i)

    selected_operation = Operation()
    print("THIS WILL NOT BE PRINTED")

    if (request.method == 'POST') and not switch:
        print("INSIDE THE SECOND POST REQUEST")
        #this variable contains the selected operation on the patient interface
        try:
            selected_operation = request.POST['selected_operation']
            print("utkarsh")
            print(selected_operation)
        except MultiValueDictKeyError:
            messages.error(request, 'Please Select an Operation')
            return redirect('chart')
    else:
        if len(operation_list) != 0:
            selected_operation = str(operation_list[0])
        print("AFTER THE ELSE CHECKING")

    #Step 1: Create a DataPool with the data we want to retrieve.
    # print(selected_operation)
    print("AFTER THE ELSE !!!!!!!!!!!!!!!")

    stepcounter_wanted_items = set()
    # cycle through all the step counter instances
    for item in StepCounter.objects.all():
        # if the logged in user is the same as the patient username who created the record
        if item.operation.patient.user.username == login_username and str(item.operation) == selected_operation:
            # then append the record to the list
            stepcounter_wanted_items.add(item.pk)
    stepcounter_filtered_data = StepCounter.objects.filter(pk__in = stepcounter_wanted_items) \
                                .values("created", "steps") \
                                .order_by('created')


    steps_data = list()

    for entry in stepcounter_filtered_data:
        t=entry['created']
        t_converted = t.timestamp()*1000
        tmp = [t_converted, entry['steps']]
        steps_data.append(tmp)

    chart = {
        'chart': {'type': 'line'},
        'title': {'text': 'Step Counter Data'},
        'xAxis': {
            'type': 'datetime',
            'dateTimeLabelFormats': { 'month': '%e. %b',
                                      'year': '%b'},
            'title' :  {
                'text': 'Date'
            },
        },
        'yAxis': {
            'title': {
                'text': 'Step Count',
            },
        },

        'plotOptions': {
        'line': {
            'marker': {
                'enabled': 'true'
            }
        }
        },

        'series': [{
        'name': 'steps',
        'data': steps_data,
    }],
    }



    #the following section creates the corresponding data needed for drawing
    #knee motion range
    kneemotionrange_wanted_items = set()

    # cycle through all the knee motion range objects
    for item in KneeMotionRange.objects.all():
        # if the logged in user is the same as the patient username who created the record
        if item.operation.patient.user.username == login_username and str(item.operation) == selected_operation:
            # then append the record to the list
            kneemotionrange_wanted_items.add(item.pk)

    kneemotionrange_filtered_data = KneeMotionRange.objects.filter(pk__in = kneemotionrange_wanted_items) \
                                .values("created", "bend", "stretch") \
                                .order_by('created')

    created_data = list()
    bend_data = list()
    stretch_data = list()

    for entry in kneemotionrange_filtered_data:
        t=entry['created']
        t_converted = t.timestamp()*1000
        tmp = [t_converted, entry['bend']]
        bend_data.append(tmp)

        tmp2 = [t_converted, entry['stretch']]
        stretch_data.append(tmp2)


    chart2 = {
        'chart': {
            'type': 'column'
         },
        'title': {'text': 'Knee Motion Data',},
        'xAxis': {
            'type': 'datetime',
            'dateTimeLabelFormats': { 'month': '%e. %b',
                                      'year': '%b'},
            'title' :  {
                'text': 'Date'
            },
        },
        'yAxis': {
            'title': {
                'text': 'Degrees',
            },
        },
        'tooltip': {
        'valueSuffix': ' degrees',
        },

        'series': [{
        'name': 'bend',
        'data': bend_data
        },
        {
        'name': 'straighten',
        'data': stretch_data
        },]
    }

    #the following section creates the corresponding data needed for drawing
    #painlevel
    painlevel_wanted_items = set()
    # cycle through all the pain level objects
    for item in PainLevel.objects.all():
        # if the logged in user is the same as the patient username who created the record
        if item.operation.patient.user.username == login_username and str(item.operation) == selected_operation:
            # then append the record to the list
            painlevel_wanted_items.add(item.pk)


    painlevel_filtered_data = PainLevel.objects.filter(pk__in = painlevel_wanted_items) \
        .values('created', 'painLevel','isMedicineTaken') \
        .order_by('created')

    with_medicine = list()
    without_medicine=list()

    for entry in painlevel_filtered_data:
        if entry['isMedicineTaken']==True:
            t=entry['created']
            t_converted = t.timestamp()*1000
            tmp = [t_converted, entry['painLevel']]
            with_medicine.append(tmp)
        else:
            t=entry['created']
            t_converted = t.timestamp()*1000
            tmp = [t_converted, entry['painLevel']]
            without_medicine.append(tmp)

    chart3 = {
        'chart': {'type': 'spline'},
        'title': {'text': 'Pain Level Data'},
        'xAxis': {'type': 'datetime',
                  'dateTimeLabelFormats': {
                  'month': '%e. %b',
                  'year': '%b'},
                  # 'labels': { 'format': '{value:%e-%b-%Y}'},
                  'title' :  {'text': 'Date'}
        },
        'yAxis': {
            'title': {
                'text': 'Pain Scores',
            },
        },

        'plotOptions': {
        'spline': {
            'marker': {
                'enabled': 'true'
            }
        }
        },

        'series': [{
        'name': 'with medicine',
        'data': with_medicine
        },
        {
        'name': 'without medicine',
        'data': without_medicine
        }
        ]
    }


    dump  = json.dumps(chart, sort_keys=True, indent=1, cls=DjangoJSONEncoder)
    dump2 = json.dumps(chart2, sort_keys=True, indent=1, cls=DjangoJSONEncoder)
    dump3 = json.dumps(chart3, sort_keys=True, indent=1, cls=DjangoJSONEncoder)

    if request.user.is_surgeon:
        switch = True
        return render(request, 'functionality/records.html', {'chart': dump, 'chart2':dump2, 'chart3':dump3,
                                                              'operation_list': operation_list,
                                                              'selected_patient_username':login_username,
                                                              'switch':switch})
    elif request.user.is_patient:
        return render(request, 'functionality/records.html', {'chart': dump, 'chart2':dump2, 'chart3':dump3,
        'operation_list': operation_list})
