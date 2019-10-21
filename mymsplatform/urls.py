"""mymsplatform URL Configuration

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
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import url
from msplt import views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^.*\.html', views.gentella_html, name='gentella'),
    path('', views.login, name='default'),
    path('login', views.login, name='login'),
    # path('register',views.register, name='register'),
    path('register', views.register, name='register'),
    path('index', views.index, name='index'),
    path('service', views.service, name='service'),
    path('node', views.node, name='node'),
    path('obtain',views.obtain,name='obtain')
    # url(r'^admin/', admin.site.urls),
    # url(r'^obtain', views.obtain)
]
