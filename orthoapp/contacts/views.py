from django.shortcuts import render, redirect
from django.core.mail import send_mail
from . models import Contact


def contact(request):
    # When the submit button is pressed by the visitor reporting the issue
    if request.method == 'POST':

        # Extract all information related to the issue (submitted by the visitor)
        info_page = request.POST['info_page']
        info_page_id = request.POST['info_page_id']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        developer_email = request.POST['developer_email']

        # Create an instance of the Contact using the given information
        contact_given = Contact(info_page=info_page, info_page_id=info_page_id, name=name, email=email, phone=phone, message=message, user_id=user_id)
        contact_given.save()

        # Send an email to the lead contact notifying them about the issue
        send_mail(
            'Information Page feedback',
            'There has been some feedback provided for ' + info_page + ' Sign in to the admin panel for more details',
            from_email='orthoapp.feedback@gmail.com',
            recipient_list=[developer_email],
            fail_silently=False
        )

        # redirect the user back to the same information page after they have made the query
        return redirect ('/information_pages/'+info_page_id)
