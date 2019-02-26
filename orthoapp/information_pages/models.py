from django.db import models
from developer.models import Developer


class Information_Page(models.Model):

    # Enumerating the options for the field surgery stage
    PRE_SURGERY     = 'PRE'
    IN_HOSPITAL     = 'HOSP'
    POST_SURGERY    = 'POST'
    LONG_TERM_CARE  = 'CARE'

    SURGERY_STAGE_CHOICES =(
    (PRE_SURGERY,    'Pre Surgery'),
    (IN_HOSPITAL,    'In Hospital'),
    (POST_SURGERY,   'Post Surgery'),
    (LONG_TERM_CARE, 'Long Term Care'),
    )

    # Enumerating the options for the field hospital name
    ORTHOPAEDICS_ACT = 'OA'
    CALVARY          = 'CL'
    HOSPITAL_CHOICES = (
    (ORTHOPAEDICS_ACT, 'Orthopaedics ACT'),
    (CALVARY,          'Calvary'),
    )

    # This field represents the developer responsible for this information page
    developer      = models.ForeignKey(Developer, on_delete = models.DO_NOTHING)

    # This represents the title of the information page
    title          = models.CharField(max_length = 200)

    # This represents the description of the information page
    description    = models.TextField(blank=True)
    
    # This represents the main text present in an information page
    main_text      = models.TextField(blank=True)

    # This represents the stage of surgery to which the information page pertains to    
    surgery_stage  = models.CharField(max_length = 20, choices = SURGERY_STAGE_CHOICES)

    # This represents the hospital name which endorses the information on this page
    hospital_name  = models.CharField(max_length = 20, choices = HOSPITAL_CHOICES)

    # This is the main photo of the information page
    photo_main     = models.ImageField(upload_to = 'photos/%Y/%m/%d/')
    
    # Each information page can have up to 4 photos 
    photo_1        = models.ImageField(upload_to = 'photos/%Y/%m/%d/', blank=True)
    photo_2        = models.ImageField(upload_to = 'photos/%Y/%m/%d/', blank=True)
    photo_3        = models.ImageField(upload_to = 'photos/%Y/%m/%d/', blank=True)
    photo_4        = models.ImageField(upload_to = 'photos/%Y/%m/%d/', blank=True)
    
    # boolean variable indicating whether a page is a key link or not
    # key links are important information pages that are available for viewing straight away from the home page
    is_key_link    = models.BooleanField(default=False)

    # boolean variable indicating whether a page is published or not 
    # pages need to be published to be viewed on the webapp   
    is_published   = models.BooleanField(default=True)

    def __str__(self):
        return self.title
