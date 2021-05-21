from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, redirect, render
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from electricity.models import electricity,Contact,FeedBack
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
import requests
import json
from django.http import HttpResponse,JsonResponse
import random
import math
# Create your views here.
def send_email_to_user(otp,email):
    import smtplib
    con = smtplib.SMTP("smtp.gmail.com",587)
    con.ehlo()
    con.starttls()
    admin_email = "email"
    admin_password = "password"
    con.login(admin_email,admin_password)
    msg = "Otp is "+str(otp)
    con.sendmail("email",email,"Subject:Password Reset \n\n"+msg)

def send_warning_email(email):
    import smtplib
    con = smtplib.SMTP("smtp.gmail.com",587)
    con.ehlo()
    con.starttls()
    admin_email = "arpit456jain@gmail.com"
    admin_password = "#jain vanshika#"
    con.login(admin_email,admin_password)
    msg = "Otp is "+str(otp)
    con.sendmail(admin_email,email,"Subject:Warning \n\n"+msg)


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
            return render(request,"login.html")
        if User.objects.filter(email=request.POST['email']).exists():
            messages.error(request, 'Email Already Exists!!')
            return render(request,"login.html")
        else:
            pass
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
                messages.success(request,"Account Created Successfully ! . Please Login.")
                return render(request,"login.html")
            else:
                messages.error(request,"Length must be greter then 8")
                return render(request,"login.html")

        else:
            messages.error(request,"Password confirmation doesn't match")
            return render(request,"login.html")

    else:
        messages.error(request,"Username Already Exist")
        return render(request,"login.html")

login_users = {}
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
                    login_users[username] = 0
                    login(request,user)
                    return redirect('/')
                else:
                    return render(request,"login.html",{"err":True})
            else:
                print("Someone tried to login and failed.")
                if username in login_users.keys():
                    login_users[username]+=1
                else:
                    login_users[username]=1
                print(login_users)
                if login_users[username] >=2:
                    user1 = User.objects.filter(username=username).first()
                    print(user1.email)
                    send_warning_email(user1.email)
                print("They used username: {} and password: {}".format(username,password))
                messages.error(request,"Wrong password or email")
                return render(request,"login.html")
        else:
            return render(request, 'login.html')

global_dict = {'otp':"",'email':"",'otpcheck':""}          
def generate_otp():
    digits = [i for i in range(0, 10)]
    random_str = ""
    for i in range(6):
        index = math.floor(random.random() * 10)
        random_str += str(digits[index])
    print(random_str,type(random_str))
    global_dict['otp'] = random_str
    send_email_to_user(random_str,global_dict['email'])
    return

def forgotp(request):
    if request.method == "POST":
        print("post")
        if User.objects.filter(email=request.POST["email"]).exists():
            print("exist")
            global_dict['email'] = request.POST["email"]
            generate_otp()
            messages.success(request, 'An otp is send to your Email please Enter that otp')
            return redirect('otp')
        else:
            messages.error(request, 'Email not Found Please Sign up First')
            return render(request,'forgotpassword.html')
    else:
        print("get")
    return render(request,'forgotpassword.html')

def otp(request):
    if request.method == "POST":
        print("post")
        get_otp = request.POST["otp"]
        if global_dict['otp'] == get_otp:
            print("match")
            global_dict['otpcheck'] = "1"
            return redirect('reset_password')
        else:
            print("otp is",global_dict['otp'])
            messages.error(request, 'Otp not Matched Please Try Again')
    else:
        print("get")
    return render(request,'otp.html')

def reset_password(request):
    if request.method == "POST":
        password = request.POST["password"]
        rpassword = request.POST["rpassword"]
        if rpassword != password:
            messages.error(request, 'Password not Matched')
        elif len(password)<=7:
            messages.error(request,"Minimum 8 characters required")
        else:
            print("matched",global_dict['email'])
            user = User.objects.filter(email=global_dict['email']).first()
            user.password = make_password(request.POST["password"])
            print(user,user.email)
            user.save()
            messages.success(request,"Password Reset Successfully! Please Login")
            return redirect("login")
    else:
        if global_dict['email'] == "":
            messages.error(request,"Please Enter your email")
            return redirect("forgotp")

        if global_dict['otp'] == "":
            messages.error(request,"Please Enter Otp first")
            return redirect("otp")
        if len(global_dict['otpcheck']) == 0:
            messages.error(request,"Otp not found")
            return redirect("otp")
            
    return render(request,'resetpassword.html')

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

@login_required
def feedback(request):
    if request.method == "POST":
        print("post")
        try:
            experience_rating = request.POST['experience_rating']
            update_rating = request.POST['update_rating']
            wating_response_rating = request.POST['wating_response_rating']
            Satisfactory_rating = request.POST['Satisfactory_rating']
            Quality_rating = request.POST['Quality_rating']
            map_rating = request.POST['map_rating']
            Announcement_rating = request.POST['Announcement_rating']
            commentText = request.POST['commentText']
            print(experience_rating)
            entry = FeedBack(experienceRating=experience_rating,updateRating=update_rating,SatisfactoryRating=Satisfactory_rating,QualityRating=Quality_rating,MapsRating=map_rating,AnnouncementsRating=Announcement_rating,waiting_for_responseRating=wating_response_rating,commentText=commentText)
            entry.save()
            messages.success(request , "Thanks for the FeedBack!")
        except:
            messages.error(request, 'Please Fill FeedBack Properly !!')
    else:
        print("Get")
    return render(request,"feedback.html")

#Contact view
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

def error_404(request, *args, **argv):
        data = {}
        return render(request,'404.html', data)
    
def check_username(request):
    username = request.GET.get("name")
    if User.objects.filter(username=username).exists():
        return JsonResponse({"exists":"yes"})
    return JsonResponse({"exists":"no"})


def check_email(request):
    email = request.GET.get("email")
    if User.objects.filter(email=email).exists():
        return JsonResponse({"exists":"yes"})
    return JsonResponse({"exists":"no"})
