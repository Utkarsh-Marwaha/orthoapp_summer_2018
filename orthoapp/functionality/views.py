from django.shortcuts import render, redirect
from functionality.forms import StepCounterForm, KneeMotionRangeForm, PainLevelForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required # login decorator that makes it easier
from accounts.decorators import patient_required, surgeon_required, practice_required
from accounts.models import Operation

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
        selected_operation = request.POST['selected_operation']

        stepcounter_form = StepCounterForm(data=request.POST)

        if stepcounter_form.is_valid:
            step_counter_object = stepcounter_form.save(commit=False)

            # Want to protect it further? do stuff below
            for j in operation_list:
                if str(j) == selected_operation:
                    step_counter_object.operation = j

            step_counter_object.save()

            submitted = True

        else:
            print(stepcounter_form.errors)
    else:
        stepcounter_form = StepCounterForm()

    return render(request, 'functionality/stepcounter.html',
    {
        'stepcounter_form' : stepcounter_form,
        'submitted'        : submitted,
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
        # selected_operation = request.POST.get('selected_operation', False)
        selected_operation = request.POST['selected_operation']
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

    return render(request, 'functionality/kneemotionrange.html',
    {
        # 'stepcounter_form' : stepcounter_form,
        'submitted'        : submitted,
        'operation_list'   : operation_list
    })

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
        selected_operation = request.POST['selected_operation']

        painlevel_form = PainLevelForm(data=request.POST)

        if painlevel_form.is_valid:
            painlevel_object = painlevel_form.save(commit=False)

            # Want to protect it further? do stuff below
            for j in operation_list:
                if str(j) == selected_operation:
                    painlevel_object.operation = j

            painlevel_object.save()

            submitted = True

        else:
            print(painlevel_form.errors)
    else:
        painlevel_form = PainLevelForm()

    return render(request, 'functionality/painlevel.html',
    {
        'painlevel_form' : painlevel_form,
        'submitted'        : submitted,
        'operation_list'   : operation_list
    })

######################## new section here #########################


from accounts.models import MyUser
from django.views.generic import View
from functionality.models import StepCounter, KneeMotionRange, PainLevel



############################## ANOTHER SECTION USING CHARTIT ###########################################
from chartit import DataPool, Chart


@login_required
@patient_required
def chart(request):
    #Step 1: Create a DataPool with the data we want to retrieve.
    print(type(StepCounter.objects.all()))
    # get the user name of the user who is currently logged in to the website
    login_username = request.user.username


    stepcounter_wanted_items = set()
    kneemotionrange_wanted_items = set()
    painlevel_wanted_items = set()



    # cycle through all the step counter instances
    for item in StepCounter.objects.all():
        print(item.operation.patient.user.username)
        # if the logged in user is the same as the patient username who created the record
        if item.operation.patient.user.username == login_username:
            # then append the record to the list
            stepcounter_wanted_items.add(item.pk)
    print("hahahhahahaa")
    print(stepcounter_wanted_items == set())
    print(stepcounter_wanted_items)

    # cycle through all the KneeMotionRange instances
    for item in KneeMotionRange.objects.all():
        print(item.operation.patient.user.username)
        # if the logged in user is the same as the patient username who created the record
        if item.operation.patient.user.username == login_username:
            # then append the record to the list
            kneemotionrange_wanted_items.add(item.pk)

    print("hehehehheheheh")
    print(kneemotionrange_wanted_items == set())
    print(kneemotionrange_wanted_items)

    # cycle through all the KneeMotionRange instances
    for item in PainLevel.objects.all():
        print(item.operation.patient.user.username)
        # if the logged in user is the same as the patient username who created the record
        if item.operation.patient.user.username == login_username:
            # then append the record to the list
            painlevel_wanted_items.add(item.pk)
    print(painlevel_wanted_items)

    stepcounter_filtered_data = StepCounter.objects.filter(pk__in = stepcounter_wanted_items)
    kneemotionrange_filtered_data = KneeMotionRange.objects.filter(pk__in = kneemotionrange_wanted_items)
    print("LOLOLOLOLOLOL")
    print(kneemotionrange_filtered_data.exists())
    painlevel_filtered_data = PainLevel.objects.filter(pk__in = painlevel_wanted_items)


    #this is to store charts that are not null
    final_list=[]

    if stepcounter_filtered_data.exists():
        stepcounter_data = \
            DataPool(
               series=
                [{'options': {
                   'source': stepcounter_filtered_data},
                  'terms': [
                    'created',
                    'steps']}
                 ])

        print("YESYESYESYESYESY")
        print(stepcounter_data)
        print(type(stepcounter_data))
        #Step 2: Create the Chart object
        stepcounter_chart = Chart(
                datasource = stepcounter_data,
                series_options =
                  [{'options':{
                      'type': 'line',
                      'stacking': False},
                    'terms':{
                      'created': [
                        'steps']
                      }}],
                chart_options =
                  {'title': {
                       'text': 'Step Counter Data of the Patient'},
                   'xAxis': {
                        'title': {
                           'text': 'Date'}}})
        final_list.append(stepcounter_chart)
    else:
        stepcounter_chart = None



    if kneemotionrange_filtered_data.exists():
        kneemotionrange_data = \
            DataPool(
               series=
                [{'options': {
                   'source': kneemotionrange_filtered_data},
                  'terms': [
                    'created',
                    'bend', 'stretch']}
                 ])

        #Step 2: Create the Chart object
        kneemotionrange_chart = Chart(
                datasource = kneemotionrange_data,
                series_options =
                  [{'options':{
                      'type': 'bar',
                      'stacking': False},
                    'terms':{
                      'created': [
                        'bend', 'stretch']
                      }}],
                chart_options =
                  {'title': {
                       'text': 'Knee Motion Range Data of the Patient'},
                   'xAxis': {
                        'title': {
                           'text': 'Date'}}})
        final_list.append(kneemotionrange_chart)

    else:
        print("IM HERERER")
        kneemotionrange_chart = None

    if painlevel_filtered_data.exists():
        painlevel_data = \
            DataPool(
               series=
                [{'options': {
                   'source': painlevel_filtered_data},
                  'terms': [
                    'created',
                    'painLevel']}
                 ])

        #Step 2: Create the Chart object
        painlevel_chart = Chart(
                datasource = painlevel_data,
                series_options =
                  [{'options':{
                      'type': 'line',
                      'stacking': False},
                    'terms':{
                      'created': [
                        'painLevel']
                      }}],
                chart_options =
                  {'title': {
                       'text': 'Pain Level Data of the Patient'},
                   'xAxis': {
                        'title': {
                           'text': 'Date'}}})
        final_list.append(painlevel_chart)

    else:
        painlevel_chart = None


    final_str = ""
    for i in range(len(final_list)):
        final_str += "chart" + (str(i+1)) + ","
    final_str = final_str[:-1]
    print(final_str)


    #Step 3: Send the chart object to the template.
    return render(request, 'functionality/records.html', {'stepcounter_chart':stepcounter_chart,
                                                          'kneemotionrange_chart':kneemotionrange_chart,
                                                          'painlevel_chart' : painlevel_chart,
                                                          'chart_list' : final_list,
                                                          'final_str' : final_str,
                                                         })
