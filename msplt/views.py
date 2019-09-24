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
    if request.session.get('is_login', None):
        return redirect('/index.html')
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        print((username, password))
        if username and password:
            username = username.strip()
            try:
                user = models.UserProfile.objects.get(name=username)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index.html')
                else:
                    message = "密码不正确！"
            except:
                message = "用户名不存在！"
            return render(request, 'login.html', {"message": message})
    return render(request, 'login.html')

def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/index.html')
    request.session.flush()
    return redirect('login.html')

def register(request):
    if request.session.get('is_login', None):
        return redirect("/index.html")
    if request.method == 'POST':
        message = '请检查填写的内容！'
        username = request.POST.get('username', None)
        password1 = request.POST.get('password1', None)
        password2 = request.POST.get('password2', None)
        email = request.POST.get('email', None)
        if username is None:
            return render(request, 'login.html', {"message": message, "signup": True})
        if password1 !=password2:
            message = '两次输入密码不同！'
            return render(request, 'login.html', {"message": message, "signup": True})
        else:
            same_name_user = models.UserProfile.objects.filter(name=username)
            if same_name_user:
                message = '用户名已经存在，请更换用户名!'
                return render(request, 'login.html', {"message": message, "signup": True})
            same_email_user = models.UserProfile.objects.filter(email=email)
            if same_email_user:
                message = '该邮箱地址已经被注册，请使用别的邮箱!'
                return render(request, 'login.html', {"message": message, "signup": True})
            new_user = models.UserProfile.objects.create()
            new_user.name = username
            new_user.password = password1
            new_user.email = email
            new_user.save()
            return redirect('login')


def gentella_html(request):
    context = {}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    template = loader.get_template(load_template)
    return HttpResponse(template.render(context, request))
