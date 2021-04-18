"""Elecktra URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from electricity import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name="home"),
    path('login/',views.loginuser,name="login"),
    path('register/',views.registeruser,name="register"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('map/',views.map,name="map"),
    path('announcements/',views.annnouncements,name="announcements"),
    path('feedback/',views.feedback,name="feedback"),
    path('logout/',views.logoutuser,name="logout"),
    path('coordinates/',views.getmapcoordinates,name="coordinates"),
    path('contact/',views.contact,name="contact"),
    path('Forgot_Password/',views.forgotp,name="forgotp"),
    path('accounts/', include('allauth.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
handler404 = 'electricity.views.error_404'
handler500 = 'electricity.views.error_404'