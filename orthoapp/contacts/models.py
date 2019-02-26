from django.db import models
from datetime import datetime

class Contact(models.Model):

    # This is the title of the information page pertaining to which the issue has been reported by the visitor
    info_page    = models.CharField(max_length=200)
    # This is the ID of the information page pertaining to which the issue has been reported by the visitor
    info_page_id = models.IntegerField()
    # The name of the visitor who reported the issue about the information page
    name         = models.CharField(max_length=200)
    # The email of the visitor who reported the issue about the information page
    email        = models.CharField(max_length=100)
    # The phone number of the visitor who reported the issue about the information page
    phone        = models.CharField(max_length=100)
    # The issue as described by the visitor
    message      = models.TextField(blank=True)
    # The date at which the issue was reported by the visitor
    contact_date = models.DateTimeField(default=datetime.now, blank=True)
    # The id of the visitor (if she was a user)
    user_id      = models.IntegerField(blank=True)

    # For easy access and greater readability, the contact shall be displayed by the visitor's name
    def __str__(self):
        return self.name
