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

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import MyUser
from django.views.generic import View
from functionality.models import StepCounter, KneeMotionRange, PainLevel

class Record(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'functionality/charts.html')

class RecordData(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated,]

    def get(self, request, format=None):
        login_username = request.user.username
        all_sc_object = StepCounter.objects.all()

        filtered_sc_object = list()
        for i in all_sc_object:
            print(i.operation.patient.user.username)
            if i.operation.patient.user.username == login_username:
                filtered_sc_object.append(i)
        print(filtered_sc_object)

        labels = list()
        default_items = list()
        for j in filtered_sc_object:
            labels.append(j.created)
            print(j.created)
            default_items.append(j.steps)

        data = {
                "labels": labels,
                "default": default_items,
        }
        return Response(data)
