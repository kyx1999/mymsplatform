from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.contrib import messages
from msplt import models
from msplt.lib import manager


# Create your views here.

# 获取节点cpu和mem
def obtain(request):
    request.encoding = 'utf-8'
    print('Return the number of node')
    file = open('describenode.txt', 'w')
    config.load_kube_config('./.kube/config')
    v1 = client.CoreV1Api()
    ret = v1.list_node(pretty=True)
    # print(ret, file=file)
    # return len(ret.items)

    all_cpu = ret.items[0].status.allocatable['cpu']  # 空载情况下cpu(资源配置相同情况下)
    all_mem = ret.items[0].status.allocatable['memory']  # 空载情况下memory
    node_list = [{'id': 'total',
                  'cpu': all_cpu,
                  'mem': all_mem}]
    capacity_cpu_sum = 0
    allocatable_cpu_sum = 0
    capacity_mem_sum = 0
    allocatable_mem_sum = 0
    for i in ret.items:
        ip = i.status.addresses[0].address
        name = i.status.addresses[1].address
        allocatable_cpu = i.status.allocatable['cpu']
        allocatable_mem = i.status.allocatable['memory']
        allocatable_mem_ = allocatable_mem[:-2]
        print(int(allocatable_mem_) / 1024 / 1024)
        capacity_cpu = i.status.capacity['cpu']
        capacity_mem = i.status.capacity['memory']
        node_list.append({'id': ip,
                          'cpu': allocatable_cpu,
                          'mem': allocatable_mem})
    # if 'q' in request.GET and request.GET['q']:
    #     message = node_list
    # else:
    #     message = 'Error!'
    message = node_list
    return HttpResponse(message)


def index(request):
    mgr = manager()
    username = request.POST.get('username', None)
    node = mgr.getNode()
    ns = mgr.getNS()
    service = mgr.getService_2()
    service_list = service['service_list']
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
    pod_ratio = int((1 - pod_num / (node_num * 110)) * 100)
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
                                          'pod_ratio': pod_ratio,
                                          'username': username,
                                          'service_list': service_list})


def service(request):
    mgr = manager()
    # username = request.POST.get('username', None)
    node = mgr.getNode()
    ns = mgr.getNS()
    service = mgr.getService_2()
    service_list = service['service_list']
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
    pod_ratio = int((1 - pod_num / (node_num * 110)) * 100)
    print(cpu_ratio)
    print(mem_ratio)
    return render(request, 'service.html', {'node_num': node_num,
                                            'ns_num': ns_num,
                                            'service_num': service_num,
                                            'pod_num': pod_num,
                                            'deployment_num': deployment_num,
                                            'node_list': node_list,
                                            'cpu_ratio': cpu_ratio,
                                            'mem_ratio': mem_ratio,
                                            'pod_ratio': pod_ratio,
                                            'service_list': service_list})


def node(request):
    mgr = manager()
    # username = request.POST.get('username', None)
    node = mgr.getNode()
    ns = mgr.getNS()
    service = mgr.getService_2()
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
    pod_ratio = int((1 - pod_num / (node_num * 110)) * 100)
    print(cpu_ratio)
    print(mem_ratio)
    return render(request, 'node.html', {'node_num': node_num,
                                         'ns_num': ns_num,
                                         'service_num': service_num,
                                         'pod_num': pod_num,
                                         'deployment_num': deployment_num,
                                         'node_list': node_list,
                                         'cpu_ratio': cpu_ratio,
                                         'mem_ratio': mem_ratio,
                                         'pod_ratio': pod_ratio,
                                         })


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


def register(request):
    if request.method == 'POST':
        message = '请检查填写的内容！'
        username = request.POST.get('username', None)
        password1 = request.POST.get('password1', None)
        password2 = request.POST.get('password2', None)
        email = request.POST.get('email', None)
        if username is None:
            return render(request, 'login.html', {"message": message, "signup": True})
        if password1 != password2:
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
