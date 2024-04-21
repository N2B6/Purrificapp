from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . models import *

class KittenUserForm(UserCreationForm):
    """
     Form for creating or updating KittenUser instances.
    """
    class Meta:
        """
        Metadata for KittenUserForm.
        """
        model = KittenUser
        fields = ['email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'phone_number', 'dob', 'address']

    def __init__(self, *args, **kwargs):
        """
        Initializer for KittenUserForm.
        """
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        """
        Save method for KittenUserForm.
        """
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

    


    
class PetForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    
    class Meta:
        model = Pet
        fields = ['name', 'pet_type', 'age', 'breed', 'description', 'image','owner']  # Replace with your specific fields
        exclude = ['owner']
    
    
    