"""ImageResizer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
import api.views
import UI.views

urlpatterns = [
    path('', UI.views.resize, name='index'),
    path('resize/', UI.views.resize, name='resize'),
    path('details/<str:task_id>/', UI.views.details, name='details'),
    path('api/resize/', api.views.rest_resize, name='rest_resize'),
    path('api/details/<str:resize_id>/', api.views.rest_details, name='rest_details'),
]
