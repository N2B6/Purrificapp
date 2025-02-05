from django.urls import path
from . import views

 
urlpatterns = [
    path('', views.home, name='Home'),
    path('about/',views.about, name='About'),
    path('FAQ/', views.FAQ , name = 'FAQ'),
    path('pets/', views.pets_view, name='all_pets'),
    path('pets/dogs/', views.pets_view, kwargs={'pet_type': 'dog'}, name='Dogs'),
    path('pets/cats/', views.pets_view, kwargs={'pet_type': 'cat'}, name='Cats'),
    path('pets/birds/', views.pets_view, kwargs={'pet_type': 'bird'}, name='Birds'),
    path('pets/fish/', views.pets_view, kwargs={'pet_type': 'fish'}, name='Fish'),
    path('pets/rodents/', views.pets_view, kwargs={'pet_type': 'rodent'}, name='Rodents'),
    path('pets/exotic/', views.pets_view, kwargs={'pet_type': 'exotic'}, name='Exotic Pets'),
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
