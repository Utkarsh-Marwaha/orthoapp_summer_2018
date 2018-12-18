from django.shortcuts import render, redirect
# from django.core.mail import send_mail
from . models import Contact

# Create your views here.
def contact(request):
    if request.method == 'POST':
        info_page = request.POST['info_page']
        info_page_id = request.POST['info_page_id']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        developer_email = request.POST['developer_email']
        contact_given = Contact(info_page=info_page, info_page_id=info_page_id, name=name, email=email, phone=phone, message=message, user_id=user_id)
        contact_given.save()

        # send_mail(
        #     'Information Page feedback',
        #     'There has been some feedback provided for' + info_page + 'Sign in to the admin panel for more details',
        #     from_email='from@gmail.com',
        #     recipient_list=[developer_email, 'to@gmail.com'],
        #     fail_silently=False
        # )

        return redirect ('/information_pages/'+info_page_id)