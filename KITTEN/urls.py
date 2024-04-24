from django.urls import path
from . import views

 
urlpatterns = [
    path('', views.home, name='Home'),
    path('about/',views.about, name='About'),
    path('FAQ/', views.FAQ , name = 'FAQ'),
    path('pets/', views.all_pets, name='all_pets'),
    path('dogs/',views.dogs, name='Dogs'),
    path('cats/',views.cats, name='Cats'),
    path('fish/',views.fish, name='Fish'),
    path('birds/',views.birds, name='Birds'),
    path('rodents/',views.rodents, name='Rodents'),
    path('exoticpets/',views.exoticpets, name='Exotic Pets'),
    path('Contact/', views.contact_view, name='Contact'),
    path('login/', views.login_view, name='Login'),
    path('terms/', views.terms, name='Terms'),
    path('register/', views.signup_view, name='Signup'),
    path('logout/', views.logout_view, name='Logout'),
    path('addlisting/', views.create_pet, name='Add Listing'),
    path('mylistings/', views.mylistings, name='My Listings'),
    path('delete_pet/<int:Pet_id>/', views.delete_pet, name='delete_pet'),
    path('events/', views.events, name='Events'),
    path('donations/', views.donations, name='Donations'),
    path('search/', views.search_pets, name='search_pets'),
    path('pet/update/<int:pet_id>/', views.update_pet, name='update_pet'),
 ]

