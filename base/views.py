from django.shortcuts import render
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
import re
from email.utils import parseaddr
from django.conf import settings
import uuid
from django.core.mail import send_mail
import random
import string


def home(request):
    rooms = Room.objects.all()
    context = {'title':'Home','active_link': 'home','room':rooms}
    return render(request,'base/index.html',context)


def about(request):
    context = {'title':'About','active_link': 'about'}
    return render(request,'base/about.html',context)

def contact(request):
    context = {'title':'Contact','active_link': 'contact'}
    return render(request,'base/contact.html',context)


def accomodation(request):
    rooms = Room.objects.all()
    special_rooms = Room.objects.filter(is_special=True)[:4]
    context = {'title':'Accomodation','active_link':'accomodation','rooms':rooms,'special_rooms':special_rooms}

    return render(request,'base/accomodation.html',context)

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('EMAIL').lower()
        password = request.POST.get('PASSWORD')

        try:
            # user = User.objects.get(email = email)
            
            # us = user_email.username
            user = authenticate(request,username=username,password=password)
            if user is None:
                user_email = User.objects.get(email = username)
                user = authenticate(request,username=user_email.username,password=password)
            if user is not None:
                profile = Profile.objects.get(user=user)
                if profile.is_verified == True:
                    login(request,user)
                    return redirect('home')
                else:
                    messages.error(request, f"Account Needs To Be Verified, Please Check Your Email")
            else:
                messages.error(request, f"Userame And Password Does Not Match.")
        except Exception as E:
            messages.error(request, f"Userame And Password Does Not Match. {E}")


    context = {'title':'Login','active_link': 'login'}
    return render(request,'base/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    if request.user.is_authenticated:
        return redirect('home')    
    if request.method == 'POST':
        try:
            regex_pattern = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,20}$'
            username = request.POST.get('USERNAME')
            email = request.POST.get('EMAIL')
            password1 = request.POST.get('PASSWORD')
            password2 = request.POST.get('PASSWORD_REPEAT')
            # if form.is_valid():
            exisitng_username = User.objects.filter(username = username).first()
            exisitng_email = User.objects.filter(email = email).first()

            if not exisitng_username and not exisitng_email:
                if re.match(r"^\S+@\S+\.\S+$",email) is not None:
                    if re.match("^[a-zA-Z0-9_.-]+$", username) is not None:
                        if re.match(regex_pattern, password1):
                            if password1 == password2:
                                user_obj = User(username = username , email = email)
                                user_obj.set_password(password1)
                                user_obj.save()
                                auth_token = str(uuid.uuid4())
                                profile_obj = Profile.objects.create(user = user_obj , auth_token = auth_token)
                                profile_obj.save()
                                send_mail_after_registration(email , auth_token)
                                return redirect('/token')
                            else:
                                messages.error(request,'Passwords do not match')
                        else:
                            if len(password1) < 8 or len(password1) > 20:
                                print("Password length should be between 8 and 20 characters.")
                                messages.error(request,'Password length should be between 8 and 20 characters.')
                            if not any(char.isdigit() for char in password1):
                                messages.error(request,'Password should contain at least one digit.')
                                print("Password should contain at least one digit.")
                            if not any(char.isalpha() for char in password1):
                                messages.error(request,'Password should contain at least one letter.')
                                print("Password should contain at least one letter.")
                            if not all(char.isalnum() or char in '@$!%*?&' for char in password1):
                                messages.error(request,'Password should contain at least one special character (@, $, !, %, *, ?, &).')
                                print("Password should contain at least one special character (@, $, !, %, *, ?, &).")

                    else:
                        messages.error(request,'Username is not valid')
                        print("Username is not valid")
                else:
                    print("Email is not valid")
                    messages.error(request,'Email is not valid')
            elif exisitng_username:
                messages.error(request,'User With This Username Already Exists,If You Think Its You Go To Login Page And Try To Login')
            elif exisitng_email:
                messages.error(request,'User With This Email Already Exists,If You Think Its You Go To Login Page And Try To Login')
            else:
                messages.error(request,'User With This Email And Username Already Exists,If You Think Its You Go To Login Page And Try To Login')
        except Exception as e:
            return HttpResponse(e)
    context = {'title':'Registration','active_link': 'register'}
    return render(request,'base/register.html',context)

def userProfile(request):
    context = {'title':'Profile','active_link': 'profile'}
    return render(request,'base/profile.html',context)


def room(request,pk):

    room = Room.objects.get(id = pk)

    context = {'title':'Room','active_link': 'room','room':room}
    return render(request,'base/detailed_page.html',context)

def booking(request,pk):

    if not request.user.is_authenticated:
        return redirect('home')    
    if request.method == 'POST':
        room = Room.objects.get(id=pk)
        user = request.user
        
        booking_code = generate_random_string(10)
        check_in = request.POST.get('CHECK_IN')
        check_out = request.POST.get('CHECK_OUT')
        adults = request.POST.get('ADULTS')
        children = request.POST.get('CHILDREN')
        price = room.price
        new_booking = Booking.objects.create(
            room=room,
            user=user,
            adults=adults,
            children=children,
            booking_code=booking_code,
            check_in_date=check_in,
            check_out_date=check_out,
            total_price=price,
            special_requests=user.email)

        new_booking.save()
        context = {'title':'Home','active_link': 'home'}
        send_mail_after_booking(user.email,booking_code)
        return render(request,'base/index.html',context)


    


def bookings(request,pk):
    bookings = Booking.objects.filter(user = pk)
    context = {'title':'My Bookings','active_link': 'bookings','bookings':bookings}
    return render(request,'base/bookings.html',context)


def generate_random_string(length):
    characters = string.ascii_letters + string.digits  # Includes uppercase letters, lowercase letters, and digits
    return ''.join(random.choice(characters) for _ in range(length))

def token_send(request):
    messages.success(request, f"An Email Has Been Send To Your Email Address Please Check")
    return redirect('login')

def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
    

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/accounts/login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('login')
        else:
            return redirect('error')
    except Exception as e:
        print(e)
        return redirect('/')

def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    # https://select-frankly-leech.ngrok-free.app
    message = f"Hi click the button to verify your account <button><a href='http`://localhost:8000/verify/{token}'>Verify</a><button>"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    html_message = message
    send_mail(
        subject,
        '',  # Use an empty string for the plain text version (optional)
        email_from,
        recipient_list,
        html_message=html_message,  # Specify the HTML content
    )
    # send_mail(subject, message , email_from ,recipient_list )

def send_mail_after_booking(email , code):
    subject = 'Booking Confirmation'
    message = f'Hi you booked a room at our hotel your booking code is {code}. Please share it with our receptionist while checking in'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )



