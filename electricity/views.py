from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

from electricity.forms import UserForm
from electricity.models import electricity
# Create your views here.

def index(request):
    return render(request,'index.html')


def registeruser(request):
    registeredcheck = False
    if(request.method == 'POST'):
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.is_active = True
            user.save()
            registeredcheck = True
            login(request,user)
            return redirect('/')
        else:
            error={"error":True}
            return render(request,"login.html",error)
    else:
        return render(request,"login.html")

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
                return render(request,"login.html",{"invalid":True})
        else:
            return render(request, 'login.html')

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
    if request.method == 'POST':
        username = request.POST['recipient-name']
        location = request.POST['message-text']
        send_mail(
            'Modified feedback form of ELECKTRA',
            'This is an demo of an issue: Acknowledging the user about future outrages. Have a look through this and update me for further modificationds',
            'sumekagarwal123@gmail.com',
            [username,'khannakshat7@gmail.com'],
            fail_silently=False
            )
        return render(request,"feedback.html")
    else:
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