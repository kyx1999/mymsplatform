import threading

from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.contrib import messages
from msplt import models
from msplt.lib import manager
from msplt.lib import postrequests
from kubernetes import client, config
import os
import datetime
import xml.dom.minidom as xmldom
import xmltodict
import json
import time
# from django.contrib.sessions.models import Session
# from django.core.cache import cache
# from django.contrib.sessions.backends.db import SessionStore
# from .forms import UploadFileForm, handle_uploaded_file
# from django.forms import ModelForm


# Create your views here.
# from mymsplatform.settings import BASE_DIR


def test(request):
    # if request.method == "POST":
    config.load_kube_config('~/.kube/config')
    v1 = client.CoreV1Api()

    suc = 1
    count = 1
    start_time = datetime.datetime.now()
    end_time = datetime.datetime.now()
    while (end_time - start_time).seconds < 7:
        pod = v1.read_namespaced_pod(name="nginx-7bb7cd8db5-b2b6h", namespace="default")
        if pod is client.V1Pod():
            suc += 1
        count += 1
        end_time = datetime.datetime.now()
        ttl_time = count / suc
    # messages.success("吞吐量(tps): " + suc / count)

    t = datetime.datetime.now()
    # service = v1.read_namespaced_service(name="nginx", namespace="default")
    service = v1.read_namespaced_pod(name="nginx-7bb7cd8db5-b2b6h", namespace="default")
    # if service is not client.V1Service():
    if service is not client.V1Pod():
        f = datetime.datetime.now()
        detal = f - t
        sec = (f - t).microseconds
        # messages.success("时延测试：" + sec)

    fd = open('user.xml')
    dom = xmltodict.parse(fd.read())
    jsonstr = json.dumps(dom, indent=1)
    str = json.loads(jsonstr)
    try:
        for i in range(0, 99):
            loginn = postrequests()
            t = threading.Thread(target=loginn.post)
            t.start()
        # messages.success(request, "创建100个协同用户成功！")
        message = "创建100个协同用户成功！"
    except Exception as e:
        # messages.warning(request, "创建100个协同用户错误！")
        message = "创建100个协同用户错误！"

    return render(request, 'test.html', {'count':count,
                                         'ttl': ttl_time,
                                         'detal': detal,
                                         'sec': sec,
                                         'msg': message})





# def test_sy(request):
#     if request.method == "POST":
#         config.load_kube_config('~/.kube/config')
#         v1 = client.CoreV1Api()
#         t = time.time()
#         service = v1.read_namespaced_service(name="nginx", namespace="default")
#         if service is not client.V1Service():
#             f = time.time()
#             sec = f - t
#             messages.success("时延测试：" + sec)



def create_thread(request):
    while True:
        config.load_kube_config('~/.kube/config')
        v1 = client.CoreV1Api()
        pod_list = v1.list_pod_for_all_namespaces()
        for i in pod_list.items:
            if i.status.phase == "Failed" or i.status.phase == "Unknown" or i.status.phase == "Pending":
                print(i.status.phase)
                # messages.add_message(request, messages.INFO, 'Hello world.')
                # messages.warning(request="有任务处于异常！")
                messages.success(request, "有任务处于异常！")
                return redirect('/index.html')


def upload(request):
    if request.method == "POST":  # 请求方法为POST时，进行处理
        my_file = request.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None
        print(my_file)
        if not my_file:
            return render(request, "form.html", {})
        destination = open(os.path.join(my_file.name), 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in my_file.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        mgr = manager()
        mgr.parse_creat()
    return redirect('/index.html')


# def multiuser(request):
#     fd = open('user.xml')
#     dom = xmltodict.parse(fd.read())
#     jsonstr = json.dumps(dom, indent=1)
#     str = json.loads(jsonstr)
#     try:
#         for i in range(0, 100):
#             loginn = postrequests()
#             t = threading.Thread(target=loginn.post)
#             t.start()
#         messages.success(request, "创建100个协同用户成功！")
#         message = "创建100个协同用户成功！"
#     except Exception as e:
#         messages.warning(request, "创建100个协同用户错误！")
#         message = "创建100个协同用户错误！"
#
#     return render(request, 'test.html', {'msg': message})

#
# def get_all_logged_in_users():
#     # 获取没有过期的session
#     sessions = Session.objects.filter(expire_date__gte=datetime.now())
#     uid_list = []
#     count = 0
#
#     # 获取session中的userid
#     for session in sessions:
#         data = session.get_decoded()
#         uid_list.append(data.get('_auth_user_id', None))
#         count += 1
#     return count
#
# #@accept_websocket
# def get_user_list(request):
#     if request.is_websocket():
#         message = request.websocket.wait()
#         while True:
#             if message:
#                 user_num = get_all_logged_in_users()
#                 request.websocket.send(str(user_num))
#                 time.sleep(10)

# def get_online_count():
#     online_ips = cache.get("online_ips", [])
#     if online_ips:
#         online_ips = cache.get_many(online_ips).keys()
#         return len(online_ips)
#     return 0


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
        node_list.append({'id': name,
                          'cpu': allocatable_cpu,
                          'mem': allocatable_mem})
    # if 'q' in request.GET and request.GET['q']:
    #     message = node_list
    # else:
    #     message = 'Error!'
    message = node_list
    return HttpResponse(message)


def index(request):
    t = threading.Thread(target=create_thread, args=(request,))
    t.start()
    mgr = manager()
    # get_user_list()
    user_num = mgr.get_all_logged_in_users()
    username = request.POST.get('username', None)
    node = mgr.getNode()
    ns = mgr.getNS()
    service = mgr.getService_2()
    service_list = service['service_list']
    pod = mgr.getPod()
    pod_list = pod['pod_list']
    # print(node)
    node_num = node['num']
    ns_num = ns['num']
    service_num = service['num']
    pod_num = pod['num']
    # print(node_num)
    node_list = node['node_list']
    cpu_ratio = node['cpu_ratio']
    mem_ratio = node['mem_ratio']

    pod_ratio = int((1 - pod_num / (node_num * 110)) * 100)

    # print(cpu_ratio)
    # print(mem_ratio)
    # print(service_list)
    return render(request, 'index.html', {'node_num': node_num,
                                          'ns_num': ns_num,
                                          'service_num': service_num,
                                          'pod_num': pod_num,
                                          'node_list': node_list,
                                          'cpu_ratio': cpu_ratio,
                                          'mem_ratio': mem_ratio,
                                          'pod_ratio': pod_ratio,
                                          'username': username,
                                          'service_list': service_list,
                                          'pod_list': pod_list,
                                          'user_num': user_num})


def pod(request):
    mgr = manager()
    username = request.POST.get('username', None)
    node = mgr.getNode()
    node_num = node['num']
    pod = mgr.getPod()
    pod_list = pod['pod_list']
    pod_num = pod['num']
    cpu_ratio = node['cpu_ratio']
    mem_ratio = node['mem_ratio']
    pod_ratio = int((1 - pod_num / (node_num * 110)) * 100)
    return render(request, 'pod.html', {'cpu_ratio': cpu_ratio,
                                        'mem_ratio': mem_ratio,
                                        'pod_ratio': pod_ratio,
                                        'pod_list': pod_list,
                                        'pod_num': pod_num,
                                        'username': username, })


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
    return render(request, 'node.html', {'node_num': node_num,
                                         'ns_num': ns_num,
                                         'service_num': service_num,
                                         'pod_num': pod_num,
                                         'deployment_num': deployment_num,
                                         'node_list': node_list,
                                         'cpu_ratio': cpu_ratio,
                                         'mem_ratio': mem_ratio,
                                         'pod_ratio': pod_ratio,
                                         'service_list': service_list
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
