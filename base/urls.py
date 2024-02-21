from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [

    path('home/',views.home,name="home"),
    path('about/',views.about,name="about"),
    path('login/',views.loginUser,name="login"),
    path('register/',views.registerUser,name="register"),
    path('logout/',views.logoutUser,name="logout"),
    path('token' , views.token_send , name="token_send"),
    path('profile' , views.userProfile , name="profile"),
    path('contact/',views.contact,name="contact"),
    path('room/<int:pk>/', views.room, name="room"),
    path('accomodation/',views.accomodation,name="accomodation"),
    path('',views.home,name="home"),
    path('verify/<auth_token>' , views.verify , name="verify"),
    path('booking/<int:pk>/', views.booking, name="booking"),
    path('bookings/<int:pk>/', views.bookings, name="booking"),


]