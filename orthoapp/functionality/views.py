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



# Create your views here.
@login_required
@patient_required
def stepcounter(request):
    submitted = False
    login_username = request.user.username
    #this list contains all the operation objects
    all_operation_list = Operation.objects.all()
    #this list contains all the operation objects filtered by login_username
    operation_list = list()
    for i in all_operation_list:
        if i.patient.user.username == login_username:
            operation_list.append(i)

    if request.method == 'POST':

        #this variable contains the selected operation on the patient interface
        try:
            selected_operation = request.POST['selected_operation']
        except MultiValueDictKeyError:
            messages.error(request, 'Please Select an Operation')
            return redirect('stepcounter')

        stepcounter_form = StepCounterForm(data=request.POST)

        if stepcounter_form.is_valid():
            step_counter_object = stepcounter_form.save(commit=False)

            # Want to protect it further? do stuff below
            for j in operation_list:
                if str(j) == selected_operation:
                    step_counter_object.operation = j

            step_counter_object.save()

            submitted = True
            messages.success(request, 'Data saved ')
            return redirect('stepcounter')

        else:
            messages.error(request, 'Invalid Data entered')
            return redirect('stepcounter')
    else:
        stepcounter_form = StepCounterForm()

    return render(request, 'functionality/stepcounter.html',
    {
        'stepcounter_form' : stepcounter_form,
        'operation_list'   : operation_list
    })
@login_required
@patient_required
def kneemotionrange(request):
    submitted = False
    login_username = request.user.username
    #this list contains all the operation objects
    all_operation_list = Operation.objects.all()
    #this list contains all the operation objects filtered by login_username
    operation_list = list()
    for i in all_operation_list:
        if i.patient.user.username == login_username:
            operation_list.append(i)

    if request.method == 'POST':
        try:
            selected_operation = request.POST['selected_operation']
        except MultiValueDictKeyError:
            messages.error(request, 'Please Select an Operation')
            return redirect('kneemotionrange')

        kneemotionrange_form = KneeMotionRangeForm()
        if kneemotionrange_form.is_valid:
            kneemotionrange_object = kneemotionrange_form.save(commit=False)
            for j in operation_list:
                if str(j) == selected_operation:
                    kneemotionrange_object.operation = j
            kneemotionrange_object.bend = float(request.POST['bend'])
            kneemotionrange_object.stretch = float(request.POST['stretch'])
            kneemotionrange_object.save()
            submitted = True
            messages.success(request, 'Data saved ')
            return redirect('kneemotionrange')

    return render(request, 'functionality/kneemotionrange.html',
    {
        'operation_list'   : operation_list
    })

PAIN_ALERT = 50
@login_required
@patient_required
def painlevel(request):
    submitted = False
    login_username = request.user.username
    #this list contains all the operation objects
    all_operation_list = Operation.objects.all()
    #this list contains all the operation objects filtered by login_username
    operation_list = list()
    for i in all_operation_list:
        if i.patient.user.username == login_username:
            operation_list.append(i)

    if request.method == 'POST':

        #this variable contains the selected operation on the patient interface
        try:
            selected_operation = request.POST['selected_operation']
        except MultiValueDictKeyError:
            messages.error(request, 'Please Select an Operation')
            return redirect('painlevel')

        painlevel_form = PainLevelForm(data=request.POST)

        if painlevel_form.is_valid():
            painlevel_object = painlevel_form.save(commit=False)

            #this is just a tmp object
            temp = Operation()

            # Want to protect it further? do stuff below
            for j in operation_list:
                if str(j) == selected_operation:
                    painlevel_object.operation = j
                    temp = j

            if PainLevel.objects.all().filter(operation=temp).count() == 0:
                print("no record yet")
                latest_painlevel_object = None
            else:
                latest_painlevel_object = PainLevel.objects.all().filter(operation=temp).latest('created')
            # print(painlevel_object)
            painlevel_object.save()

            ##########check for 2 consecutive pain level scores of 7 within the last seven hours##############################
            if latest_painlevel_object is not None:
                latest_painlevel = latest_painlevel_object.painLevel
                latest_created = latest_painlevel_object.created

                current_painlevel = painlevel_object.painLevel
                current_created = painlevel_object.created

                pain_level_hours = 7
                pain_level_threshold = 7
                different = current_created - latest_created

                if different.days == 0 and different.seconds <= pain_level_hours*60*60 and current_painlevel >=pain_level_threshold and latest_painlevel >=pain_level_threshold:
                    messages.success(request, 'Data saved')
                    messages.add_message(request, PAIN_ALERT,"You might like to contact your G.P about your pain")
                    return redirect('painlevel')
                else:
                    submitted = True
                    messages.success(request, 'Data saved ')
                    return redirect('painlevel')
            else:
                messages.success(request, 'Data saved ')
                return redirect('painlevel')

        else:
            messages.error(request, 'Invalid Data entered')
            return redirect('painlevel')
    else:
        painlevel_form = PainLevelForm()

    return render(request, 'functionality/painlevel.html',
    {
        'painlevel_form' : painlevel_form,
        'operation_list' : operation_list
    })

######################## new section here #########################


from accounts.models import MyUser
from django.views.generic import View
from functionality.models import StepCounter, KneeMotionRange, PainLevel



############################## ANOTHER SECTION USING CHARTIT ###########################################
import json
from django.db.models import Count, Q
from django.core.serializers.json import DjangoJSONEncoder

@login_required
def chart(request):

    login_username = ""

    switch=False

    if request.method == "POST":
        if 'switch' in request.POST:
            switch = request.POST["switch"]




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
                                .values("created", "steps")

    created_data = list()
    steps_data = list()

    for entry in stepcounter_filtered_data:
        created_data.append(entry['created'])
        steps_data.append(entry['steps'])

    chart = {
        'chart': {'type': 'line'},
        'title': {'text': 'Step Counter Data'},
        'xAxis': {
        'categories' : [created_data], 'title' :  {'text': 'Date'}
        },
        'yAxis': {
            'title': {
                'text': 'Step Count',
            },
        },
        'series': [{
        'name': 'steps',
        'data': steps_data,
    }],
    }


    #Step 1: Create a DataPool with the data we want to retrieve.

    kneemotionrange_wanted_items = set()

    # cycle through all the knee motion range objects
    for item in KneeMotionRange.objects.all():
        # if the logged in user is the same as the patient username who created the record
        if item.operation.patient.user.username == login_username and str(item.operation) == selected_operation:
            # then append the record to the list
            kneemotionrange_wanted_items.add(item.pk)

    kneemotionrange_filtered_data = KneeMotionRange.objects.filter(pk__in = kneemotionrange_wanted_items) \
                                .values("created", "bend", "stretch")

    created_data = list()
    bend_data = list()
    stretch_data = list()

    for entry in kneemotionrange_filtered_data:
        created_data.append(entry['created'])
        bend_data.append(entry['bend'])
        stretch_data.append(entry['stretch'])

    chart2 = {
        'chart': {
            'type': 'column'
         },
        'title': {'text': 'Knee Motion Data',},
        'xAxis': {
            'categories' : [created_data],
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

    #Step 1: Create a DataPool with the data we want to retrieve.

    painlevel_wanted_items = set()
    # cycle through all the pain level objects
    for item in PainLevel.objects.all():
        # if the logged in user is the same as the patient username who created the record
        if item.operation.patient.user.username == login_username and str(item.operation) == selected_operation:
            # then append the record to the list
            painlevel_wanted_items.add(item.pk)

    painlevel_filtered_data = PainLevel.objects.filter(pk__in = painlevel_wanted_items) \
                                .values("created", "painLevel")

    created_data = list()
    painlevel_data = list()

    for entry in painlevel_filtered_data:
        created_data.append(entry['created'])
        painlevel_data.append(entry['painLevel'])


    chart3 = {
        'chart': {'type': 'line'},
        'title': {'text': 'Pain Level Data'},
        'xAxis': {
        'categories' : [created_data], 'title' :  {'text': 'Date'}
        },
        'yAxis': {
            'title': {
                'text': 'Pain Scores',
            },
        },
        'series': [{
        'name': 'painlevel',
        'data': painlevel_data,
    }]
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
