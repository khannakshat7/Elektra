from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.forms import UserCreationForm
from electricity.models import electricity
# Create your views here.

def index(request):
    return render(request,'index.html')


def registeruser(request):
    if not User.objects.filter(username=request.POST["username"]).exists():
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
                context="Wrong Email or Password"
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

@login_required
def feedback(request):
    return render(request,"feedback.html")

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

