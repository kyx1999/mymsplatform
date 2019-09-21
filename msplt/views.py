from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.contrib import messages
from msplt import models

# Create your views here.


def index(request):
    pass
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        print((username, password))
        if username and password:
            username = username.strip()
            try:
                user = models.UserProfile.objects.get(name=username)
                if user.password == password:
                    return redirect('/index.html')
                else:
                    message = "密码不正确！"
            except:
                message = "用户名不存在！"
            return render(request, 'login.html', {"message": message})
    return render(request, 'login.html')


def gentella_html(request):
    context = {}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    template = loader.get_template(load_template)
    return HttpResponse(template.render(context, request))
