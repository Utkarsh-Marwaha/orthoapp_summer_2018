from django.db import models

# Create your models here.

class Developer(models.Model):
    name = models.CharField(max_length = 200)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    description = models.TextField(blank=True)
    phone = models.CharField(max_length= 20)
    email = models.CharField(max_length= 50)
    is_lead_contact = models.BooleanField(default=False)

    def __str__(self):
        return self.name
        
