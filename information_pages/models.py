from django.db import models
from practice.models import Practice

# Create your models here.
class Information_Page(models.Model):
    PRE_SURGERY = 'PRE'
    POST_SURGERY  = 'PST'
    SURGERY_STAGE_CHOICES =(
    (PRE_SURGERY, 'Pre Surgery'),
    (POST_SURGERY, 'Post Surgery'),
    )

    ORTHOPAEDICS_ACT = 'OA'
    CALVARY  = 'CL'
    HOSPITAL_CHOICES =(
    (ORTHOPAEDICS_ACT, 'Orthopaedics ACT'),
    (CALVARY, 'Calvary'),
    )


    practice       = models.ForeignKey(Practice, on_delete = models.DO_NOTHING)
    title          = models.CharField(max_length = 200)
    description    = models.TextField(blank=True)
    surgery_stage  = models.CharField(max_length = 10, choices = SURGERY_STAGE_CHOICES)
    hospital_name  = models.CharField(max_length = 20, choices = HOSPITAL_CHOICES)
    photo_main     = models.ImageField(upload_to = 'photos/%Y/%m/%d/')
    photo_1        = models.ImageField(upload_to = 'photos/%Y/%m/%d/', blank=True) 
    photo_2        = models.ImageField(upload_to = 'photos/%Y/%m/%d/', blank=True) 
    photo_3        = models.ImageField(upload_to = 'photos/%Y/%m/%d/', blank=True) 
    photo_4        = models.ImageField(upload_to = 'photos/%Y/%m/%d/', blank=True) 
    is_key_link    = models.BooleanField(default=False)
    is_published   = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title