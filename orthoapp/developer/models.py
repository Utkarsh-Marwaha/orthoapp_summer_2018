from django.db import models


class Developer(models.Model):
    
    # The name of the developer 
    name = models.CharField(max_length = 200)

    # The profile picture of the Developer
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)

    # A brief summary about the developer's role
    description = models.TextField(blank=True)

    # phone number of the developer
    phone = models.CharField(max_length= 20)

    # email of the developer 
    email = models.CharField(max_length= 50)

    # boolean variable indicating whether the developer is the lead contact or not 
    is_lead_contact = models.BooleanField(default=False)

    def __str__(self):
        return self.name
        
