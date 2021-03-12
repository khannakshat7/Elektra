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
    if request.POST.get("form_two"):
            if not User.objects.filter(username=request.POST["username"]).exists():
                if request.POST["password"]==request.POST["rpassword"]:
                    data=User()
                    data.password=make_password(request.POST["password"])
                    data.first_name=request.POST["first_name"]
                    data.last_name=request.POST["last_name"]
                    data.username=request.POST["username"]
                    data.email = request.POST["email"]
                    data.is_active = True
                    print("user saved")
                    data.save()
                    
                    return redirect('/login/')
                else:
                    context="Password confirmation doesn't match Password"
                    print("wrong password")
                    return render(request,"login.html",{'errorP':context})

            else:
                context="Email Already Exist"
                return render(request,"login.html",{'errorE':context})
                

    else:
        return render(request,"login.html")

def loginuser(request):

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
            return render(request,"login.html",{"invalid":True})
    else:
        return render(request, 'login.html')

def forgotp(request):
        if(request.method=="POST"):
            if  User.objects.filter(username=request.POST["username"]).exists():
                if User.objects.filter(first_name= request.POST["first_name"]).exists():
                    if User.objects.filter(last_name=request.POST["last_name"]).exists():
                        data=User(request.POST["username"])
                        
                        if request.POST["password"]==request.POST["rpassword"]:
                            data.first_name=request.POST["first_name"]
                            data.last_name=request.POST["last_name"]
                            data.username=request.POST["username"]
                            data.password=make_password(request.POST["password"])
                            data.is_active = True
                            print("user saved")
                            data.save()
                            return redirect('/')
                        else:
                            context="Password confirmation doesn't match Password"  
                            return render(request,'forgotpassword.html' ,{'ErrorFP':context})
                    else:
                        context="Wrong Surname"  
                        return render(request,'forgotpassword.html' ,{'ErrorWs':context})
                else:
                    context="Wrong First Name"
                    return render(request,'forgotpassword.html', {'ErrorFP':context})
            else:
                context="Wrong Email"  
                return render(request,'forgotpassword.html' ,{'ErrorEmail':context})
                
        else:
            print("bc")
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