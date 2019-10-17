from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.contrib import messages
from msplt import models
from msplt.lib import manager

# Create your views here.


def index(request):
    mgr = manager()
    node = mgr.getNode()
    ns = mgr.getNS()
    service = mgr.getService()
    pod = mgr.getPod()
    deployment = mgr.getDeployment()
    # print(node)
    node_num = node['num']
    ns_num = ns['num']
    service_num = service['num']
    pod_num = pod['num']
    # print(node_num)
    node_list = node['node_list']
    cpu_ratio = node['cpu_ratio']
    mem_ratio = node['mem_ratio']
    deployment_num = deployment['num']
    pod_ratio = int((1-pod_num/(node_num*110))*100)
    print(cpu_ratio)
    print(mem_ratio)
    return render(request, 'index.html', {'node_num': node_num,
                                          'ns_num': ns_num,
                                          'service_num': service_num,
                                          'pod_num': pod_num,
                                          'deployment_num': deployment_num,
                                          'node_list': node_list,
                                          'cpu_ratio': cpu_ratio,
                                          'mem_ratio': mem_ratio,
                                          'pod_ratio': pod_ratio})

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
                    return redirect('/index')
                else:
                    message = "密码不正确！"
            except:
                message = "用户名不存在！"
            return render(request, 'login.html', {"message": message})
    return render(request, 'login.html')

def register(request):
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
