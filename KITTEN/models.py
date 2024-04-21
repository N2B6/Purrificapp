from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


    
class KittenUser(AbstractUser):
    """
    Custom user model for the Wanderlust app.

    Inherits from Django's AbstractUser model and adds custom fields.
    """
    address = models.CharField(_("address"), max_length=255, null=True, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    phone_number = models.CharField(_("phone number"), max_length=15, null=True, blank=True)
    dob = models.DateField(_("date of birth"), null=True, blank=True)
    

    # Meta class to specify custom permissions
    class Meta:
        """
        Meta options for the KittenUser model.

        Specifies the name of the model and a custom permission.
        """

        permissions = (("can_access_dashboard", "Can access dashboard"),)

    def save(self, *args, **kwargs):
        """
        Save the user instance with custom logic.

        Sets the username field to the email address if it is not set.
        """
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        """
        Return the username of the user.

        Used for string representation of the user object.
        """
        return self.username


class Pet(models.Model):
    PET_TYPES = (
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('fish', 'Fish'),
        ('rodent', 'Rodent'),
        ('exotic', 'Exotic'),
        # Add more types as needed
    )
    name = models.CharField(max_length=100)
    pet_type = models.CharField(max_length=50, choices=PET_TYPES, null=False, default='dog')
    age = models.FloatField()
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    owner = models.ForeignKey(KittenUser, null = True, on_delete=models.CASCADE)
    # listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='pets')
    image = models.ImageField(upload_to='KITTEN/images', null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name   
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Event(models.Model):
    event_name = models.CharField(max_length=100, null = False, blank = False)
    event_description = models.TextField()
    event_date = models.DateField(null = False, blank = False)
    event_time = models.TimeField(null = False, blank = False)
    event_location = models.CharField(max_length=100, null = False, blank = False)
    event_host = models.CharField(max_length=100, null = False, blank = False)
    event_image = models.ImageField(null=False)
    def __str__(self):
        return self.event_name
    

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    def __str__(self):
        return self.name
        
        
