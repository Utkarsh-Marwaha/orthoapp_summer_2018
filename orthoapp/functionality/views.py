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
        stepcounter_form = StepCounterForm(data=request.POST)

        if stepcounter_form.is_valid:
            step_counter_object = stepcounter_form.save(commit=False)

            # Want to protect it further? do stuff below

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

def kneemotion(request):
    pass

def painlevel(request):
    pass
