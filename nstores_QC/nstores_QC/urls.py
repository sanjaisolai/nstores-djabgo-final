"""
URL configuration for nstores_QC project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/upload/<str:type>/<str:packaged>/', views.upload, name='upload'),
    path('spell_check/<word>', views.spellcheck, name='spellcheck'),
    path('spellLong/<word>', views.spellL, name='spellL'),
    path('First_Letter', views.firstLetter, name='firstLetter'),
    path('length', views.length, name='length'),
    path('image_quality', views.image_quality, name='image_quality'),
    path('fssai_check',views.fssai,name='fssai'),
    path('progress',views.progress,name='progress'),
    path('display_image',views.display_image,name='display_image')
]
