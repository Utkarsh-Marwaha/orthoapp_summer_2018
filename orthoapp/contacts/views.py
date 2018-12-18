from django.shortcuts import render, redirect
from . models import Contact

# Create your views here.
def contact(request):
    if request.method == 'POST':
        info_page = request.POST['info_page']
        info_page_id = request.POST['info_page_id']
        name= request.POST['name']
        email= request.POST['email']
        phone= request.POST['phone']
        message= request.POST['message']
        user_id= request.POST['user_id']
        developer_email= request.POST['developer_email']

        contact= Contact(info_page=info_page, info_page_id=info_page_id, name=name, email=email, phone=phone, message=message, user_id=user_id)

        contact.save()

        return redirect ('/information_pages/'+info_page_id)