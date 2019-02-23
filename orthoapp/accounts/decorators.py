from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

'''
Decorator for views that checks that the logged in user is a patient,
redirects to the log-in page if necessary.
'''
def patient_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='user_login'):

    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_patient,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

'''
Decorator for views that checks that the logged in user is a surgeon,
redirects to the log-in page if necessary.
'''
def surgeon_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='user_login'):

    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_surgeon,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

'''
Decorator for views that checks that the logged in user is a practice,
redirects to the log-in page if necessary.
'''
def practice_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='user_login'):

    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_practice,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

""" 
    Reference: https://simpleisbetterthancomplex.com/tutorial/2018/01/18/how-to-implement-multiple-user-types-with-django.html
"""