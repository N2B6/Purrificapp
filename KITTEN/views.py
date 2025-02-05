from django.shortcuts import render, redirect, get_object_or_404
from .forms import KittenUserForm 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PetForm,PetUpdateForm
from django import forms
from .models import Pet , Event, Contact, KittenUser
from django.http import HttpResponseRedirect
import boto3
from .petsearch import *

# Create your views here.
def home(request):
    return render (request, 'home.html')

def about(request):
    return render (request, 'about.html')

def dogs(request):
    dogs = filter_pets_by_type('dog')
    return render(request, 'categories/dogs.html', {'dog': dogs})

def cats(request):
    cats = filter_pets_by_type('cat')
    return render(request, 'categories/cats.html', {'cat': cats})

def fish(request):
    fish = filter_pets_by_type('fish')
    return render(request, 'categories/fish.html', {'fish': fish})

def birds(request):
    birds = filter_pets_by_type('bird')
    return render(request, 'categories/birds.html', {'bird': birds})

def rodents(request):
    rodents = filter_pets_by_type('rodent')
    return render(request, 'categories/rodents.html', {'rodent': rodents})

def exoticpets(request):
    exoticpets = filter_pets_by_type('exotic')
    return render(request, 'categories/exoticpets.html', {'exoticpet': exoticpets})
    
def all_pets(request):
    pets = Pet.objects.all().order_by('-created_at')
    return render(request, 'pets.html', {'pets': pets})

def search_pets(request):
    query = request.GET.get('query')
    sort_by = request.GET.get('sort_by')

    if query:
        pets_by_name = search_pets_by_name(query)
        pets_by_breed = search_pets_by_breed(query)
        pets_by_type = search_pets_by_type(query)
        pets = pets_by_name.union(pets_by_breed, pets_by_type)
    else:
        pets = Pet.objects.all()

    # Sort the queryset based on the selected option
    if sort_by:
        if sort_by == 'age':
            pets = sorted(pets, key=lambda x: x.age)
        elif sort_by == 'latest':
            pets = pets.order_by('-created_at')
        elif sort_by == 'oldest':
            pets = pets.order_by('created_at')

    return render(request, 'pets.html', {
        'pets': pets,
        'query': query,
        'sort_by': sort_by
    })

def mylistings(request):
    user_pet_listings = Pet.objects.filter(owner=request.user)
    return render(request, 'mylistings.html', {'user_pet_listings': user_pet_listings})

def update_pet(request, pet_id):
    pet = get_object_or_404(Pet, pk=pet_id)
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('My Listings')  # Redirect to the listings page after updating
    else:
        form = PetForm(instance=pet)
    return render(request, 'update_pet.html', {'form': form, 'pet': pet})

# def newuserform(request):
#     return render (request, 'forms/newuserform.html')


def FAQ(request):
    return render (request, 'FAQ.html')
    
    
def terms(request):
    return render (request, 'terms.html')


from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import KittenUserForm

def signup_view(request):
    if request.method == "POST":
        form = KittenUserForm(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')

            if password1 == password2:
                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                dob = form.cleaned_data.get('dob')
                address = form.cleaned_data.get('address')
                phone_number = form.cleaned_data.get('phone_number')

                user = form.save(commit=False)
                user.email = email
                user.first_name = first_name
                user.last_name = last_name
                user.address = address
                user.dob = dob
                user.phone_number = phone_number
                user.save()

                user = authenticate(username=username, password=password1)
                if user is not None:
                    login(request, user)
                    return redirect('Home')
            else:
                form.add_error('password2', 'Passwords do not match')
    else:
        form = KittenUserForm()

    return render(request, 'register.html', {'form': form})





def logout_view(request):
    logout(request)
    return redirect('Home')  # Redirect to your desired page

from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)  # Create the form
        if form.is_valid():  # Validate the form
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)  # Authenticate user
            if user is not None:
                login(request, user)  # Log in the user
                return redirect('Home')  # Redirect to the homepage or any other desired page
            else:
                messages.error(request, 'Invalid email or password.')  # Display error message
        else:
            messages.error(request, 'Invalid email or password.')  # Display error message
            return render(request, 'login.html', {'login_failed': True})  # Set login_failed to True
            # Handle form validation errors 
    else:
        form = AuthenticationForm()  # Create an empty form for GET requests

    context = {'form': form, 'is_logged_in': request.user.is_authenticated, 'username': request.user.username if request.user.is_authenticated else None}
    
    return render(request, 'login.html', context)  # Render the login template



@login_required
def create_pet(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)  # Save the form data but don't commit to the database yet
            pet.owner = request.user  # Set the owner to the current logged-in user
            pet.save()  # Now save the pet object with the owner assigned
            messages.success(request, 'Pet created successfully!')  # Add success message
            print(f"Pet created successfully! Details: {form.cleaned_data}")  # Print success message with details
            return redirect('Home')  # Redirect to the home page
        else:
            print(form.errors)  # Print errors for debugging
    else:
        form = PetForm()
    context = {'addpetform': form}
    return render(request, 'pet_form.html', context)



@login_required
def delete_pet(request, Pet_id):
    # Retrieve the pet object to delete
    pet_to_delete = get_object_or_404(Pet, pk=Pet_id)
    
    # Check if the user is the owner of the pet listing
    if pet_to_delete.owner == request.user:
        # Delete the pet listing
        pet_to_delete.delete()
        return redirect('My Listings')
    else:
        # Return an error message or handle unauthorized deletion
        # For example:
        return render(request, 'error.html', {'message': 'You are not authorized to delete this pet listing.'})




def events(request):
    event = Event.objects.all()
    context = {'events': event}
    return render(request, 'events.html', context)
    



def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Save contact info to the database
        contact = Contact.objects.create(name=name, email=email, phone=phone, message=message)

        # Send confirmation email using SNS
        sns = boto3.client('sns', region_name='eu-west-1')  # Replace 'your-region' with your AWS region
        topic_arn = 'arn:aws:sns:eu-west-1:250738637992:purrificcontactus'  # Replace 'your-topic-arn' with your SNS topic ARN
        
        # Check if the email is already subscribed to the SNS topic
        subscriptions = sns.list_subscriptions_by_topic(TopicArn=topic_arn)
        subscribed_emails = [sub['Endpoint'] for sub in subscriptions['Subscriptions'] if sub['Protocol'] == 'email']

        if email not in subscribed_emails:
            # Subscribe the user's email to the SNS topic
            sns.subscribe(
                TopicArn=topic_arn,
                Protocol='email',
                Endpoint=email
            )

            # Add success message for subscription
            messages.success(request, 'Your email has been subscribed to our mailing list. Please check your email to confirm the subscription.')

        # Send confirmation message for contacting us
        sns.publish(TopicArn=topic_arn, Message=f"Thank you for contacting us, {name}! We will get back to you as soon as possible")

        # Add success message for contacting us
        messages.success(request, 'Your message has been submitted successfully!')

        # Redirect to the same page to prevent duplicate form submissions
        return redirect('Contact')  # Assuming the URL name for the contact page is 'contact'
    else:
        return render(request, 'contact.html')



def donations(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message', '')

        print(f"Amount: {amount}")
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Message: {message}")

        # Send confirmation email using SNS
        sns = boto3.client('sns', region_name='eu-west-1')  # Replace 'your-region' with your AWS region
        topic_arn = 'arn:aws:sns:eu-west-1:250738637992:purrificcontactus'  # Replace 'your-topic-arn' with your SNS topic ARN
        
        # Check if the email is already subscribed to the SNS topic
        subscriptions = sns.list_subscriptions_by_topic(TopicArn=topic_arn)
        subscribed_emails = [sub['Endpoint'] for sub in subscriptions['Subscriptions'] if sub['Protocol'] == 'email']

        if email not in subscribed_emails:
            # Subscribe the user's email to the SNS topic
            print("Subscribing email...")
            sns.subscribe(
                TopicArn=topic_arn,
                Protocol='email',
                Endpoint=email
            )

            # Add success message for subscription
            messages.success(request, 'Your email has been subscribed to our mailing list. Please check your email to confirm the subscription.')

        # Send confirmation message for donation
        print("Sending confirmation message...")
        sns.publish(TopicArn=topic_arn, Message=f"Thank you for your donation, {name}! Your contribution of €{amount} is greatly appreciated.")

        # Add success message for donation
        messages.success(request, 'Thank you for your donation!')

        # Redirect to the same page to prevent duplicate form submissions
        return redirect('Donations')  # Assuming the URL name for the donate page is 'Donations'
    else:
        return render(request, 'donations.html')

from django.shortcuts import render
from .models import Pet
from .petsearch import filter_pets_by_type

def pets_view(request, pet_type=None):
    """
    A unified view to handle all pet categories
    
    Args:
        request: The HTTP request
        pet_type: Optional pet type to filter by (dog, cat, bird, etc.)
    """
    # Get all pets or filter by type if specified
    if pet_type:
        pets = filter_pets_by_type(pet_type)
    else:
        pets = Pet.objects.all().order_by('-created_at')

    # Pass category-specific title and description
    context = {
        'pets': pets,
        'category': {
            'title': pet_type.upper() if pet_type else 'ALL PETS',
            'description': get_category_description(pet_type)
        }
    }
    
    return render(request, 'pets.html', context)

def get_category_description(pet_type):
    """Helper function to get category descriptions"""
    descriptions = {
        'dog': 'A loyal and affectionate companion',
        'cat': 'Independent nature and graceful demeanor, a charming companion',
        'bird': 'Colorful plumage and melodic songs bring joy and companionship',
        'fish': 'Bringing serenity and elegance to any aquatic environment',
        'rodent': 'Adorable antics and compact size, delightful pocket pets',
        'exotic': 'Unique characteristics and specialized care needs',
        None: 'Find your perfect companion'
    }
    return descriptions.get(pet_type, '')
