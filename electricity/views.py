from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, redirect, render
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from electricity.models import electricity,Contact,Feedback
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
import requests
import json
# Create your views here.

def index(request):
    return render(request,'index.html')

def registeruser(request):
    if not User.objects.filter(username=request.POST["username"]).exists():
        recaptcha_response = request.POST.get("g-recaptcha-response")
        url = "https://www.google.com/recaptcha/api/siteverify"
        data = {
                'secret': "6LfEWpIaAAAAAIJ0DdQCVxe_w5v4tAjyj6Quqp5v",
                'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        if result['success']==False:
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if request.POST["password"]==request.POST["rpassword"]:
            if (len(request.POST["password"]) > 7):
                data=User()
                data.password=make_password(request.POST["password"])
                data.first_name=request.POST["first_name"]
                data.last_name=request.POST["last_name"]
                data.username=request.POST["username"]
                data.email = request.POST["email"]
                data.is_active = True
                print("user saved")
                data.save() 
                return render(request,"login.html")
            else:
                context="Length must be greter then 8"
                return render(request,"login.html",{'errorP':context})

        else:
            context="Password confirmation doesn't match"
            print("wrong password")
            return render(request,"login.html",{'errorPC':context})

    else:
        context="Email Already Exist"
        return render(request,"login.html",{'errorE':context})

def loginuser(request):
    if request.user.is_authenticated:
        print("Already Logged in")
        return redirect("dashboard")
    else:
        if(request.method == 'POST'):
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request,user)
                    return redirect('/')
                else:
                    return render(request,"login.html",{"err":True})
            else:
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(username,password))
                context="Wrong password or email"
                return render(request,"login.html",{"invalid":context})
        else:
            return render(request, 'login.html')

def forgotp(request):
    if(request.method=="POST"):
        if User.objects.filter(username=request.POST["username"]).exists():
            user= User.objects.filter(username=request.POST["username"])
            for object in user:
                if object.first_name==request.POST["first_name"]:
                    if object.last_name==request.POST["last_name"]:
                        if request.POST["password"]==request.POST["rpassword"]:
                            object.password=make_password(request.POST["password"])
                            object.save()
                            print('done')
                            messages.success(request,"Password Changed")
                            return redirect('/login/')
                        else:
                            context="Password confirmation doesn't match"
                            return render(request,'forgotpassword.html',{'ErrorFP':context})
                    else:
                        context="Wrong First Name"
                        return render(request,'forgotpassword.html',{'ErrorFN':context})
                else:
                    context="Wrong Last Name"
                    return render(request,'forgotpassword.html',{'ErrorLN':context})
        else:
            context="Email not found"
            return render(request,'forgotpassword.html',{'ErrorEmail':context})
    else:
        return render(request,'forgotpassword.html')

def logoutuser(request):
    logout(request)
    return redirect('/')

@login_required
def dashboard(request):
    return render(request,"dashboard.html")

@login_required
def map(request):
    records = electricity.objects.all()
    return render(request,"map.html",{"data":records})

@login_required
def annnouncements(request):
    return render(request,"announcements.html")

# feedback view
@login_required
def feedback(request):
    if request.method == 'POST':
        try:
            form_data = request.POST
            if request.user.email:
                user_email = request.user.email
            else:
                user_email = None
            new_feedback = Feedback(overall_experience=form_data['overall_experience'],
                            time_to_time_update=form_data['time_to_time_update'],
                            experience_due_to_delay=form_data['experience_due_to_delay'],
                            visuals_satisfactory=form_data['visuals_satisfactory'],
                            quality_of_work=form_data['quality_of_work'],
                            experience_of_display_maps=form_data['experience_of_display_maps'],
                            experience_of_announcements_section=form_data['experience_of_announcements_section'],
                            others_suggestions=form_data['others_suggestions'],
                            user_email=user_email)
            new_feedback.save()
            messages.success(request, 'Thank You, your feedback response is saved. We will respond you as soon as possible !')
        except Exception as e:
            messages.error(request, 'Sorry, your feedback response is not saved. Please try again !')
        return redirect('feedback')
    return render(request, "feedback.html")

#Cobtact view
def contact(request):
    if request.method == "POST":
        recaptcha_response = request.POST.get("g-recaptcha-response")
        url = "https://www.google.com/recaptcha/api/siteverify"
        data = {
                'secret': "6LfEWpIaAAAAAIJ0DdQCVxe_w5v4tAjyj6Quqp5v",
                'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        if result['success']==False:
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        name = request.POST['name']
        message = request.POST['message']
        contact = Contact(name=name,email=email,phone=phone,message=message)
        contact.save()
        subject = name + ' wants to contact you'
        send_mail(subject,message,email,['your_gmail@gmail.com'],fail_silently=False)
    return render(request,"contact.html")

@csrf_exempt
def getmapcoordinates(request):
    if(request.method == 'POST'):
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        if(len(latitude) and len(longitude)):
            data = electricity()
            data.latitude = latitude
            data.longitude = longitude
            data.save()
        return redirect('map')

