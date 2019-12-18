import random

from kubernetes.client.rest import ApiException
from kubernetes import client, config, watch
import time
import json
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone
import requests
import threading
import uuid
from datetime import datetime
from datetime import timedelta

from mymsplatform.settings import BASE_DIR





class postrequests():
    def __init__(self):
        # 产生UUID
        u = uuid.uuid1()
        # 产生订单编号
        orderID = 'TEST' + u.hex
        self.url = 'http://127.0.0.1:8000'
        self.data = {"csrfmiddlewaretoken": "E3OKPqmHQyt6MLaMfFArSsBJNo7pllgsEn6iFHqk5pGEURqm12a58b7VfG40TnsG",
                     "username": "1234", "password": "1234"}
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept - Encoding': 'gzip, deflate, br',
            'Accept - Language': 'zh-CN, zh; q=0.9',
            'Cache - Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content - Length': '112',
            'Content - Type': 'application/x-www-form-urlencoded',
            'Cookie': 'csrftoken = i3egm2oEU39XnMmqubsUNHMOI9OkjNDwinwOcjsh9UmvvSC0gy2y3qi0arLVRPPK',
            'Host': '127.0.0.1:8000',
            'Origin': 'http://127.0.0.1:8000',
            'Referer': 'http://127.0.0.1: 8000/',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }

    def post(self):
        try:
            r = requests.post(self.url, self.data, headers=self.headers)
            print(r.text)
        except Exception as e:
            print(e)


class manager(object):
    def __init__(self):
        # config.load_kube_config('E:/pythonProject/test/resource/config')
        config.load_kube_config(
            '~/.kube/config')  # kubectl config view -- to find the config position to replace this line
        self.core_v1 = client.CoreV1Api()
        self.apps_v1 = client.AppsV1Api()

    def get_all_logged_in_users(self):
        # Query all non-expired sessions
        # use timezone.now() instead of datetime.now() in latest versions of Django
        sessions = Session.objects.filter(expire_date__gte=timezone.now())
        uid_list = []
        # Build a list of user ids from that query
        for session in sessions:
            data = session.get_decoded()
            uid_list.append(data.get('_auth_user_id', None))
        # Query all logged in users based on id list
        if len(User.objects.filter(id__in=uid_list)) == 0:
            return 0
        return len(User.objects.filter(id__in=uid_list))

        # def parse_creat(self):
        # data = json.load(open("file.json", "r"))
        # for name, nodelist in data:
        #     pod = client.V1Pod()
        #     pod.metadata = client.V1ObjectMeta(name=(name + str(random.randint(0, 1000))))
        #     container = client.V1Container(image=name, name=name)
        #     container.image = name
        #     container.name = name
        #     spec = client.V1PodSpec()
        #     spec.containers = [container]
        #     for node_name in nodelist:
        #         spec.node_name = node_name
        #         pod.spec = spec
        #         self.core_v1.create_namespaced_pod(namespace="default", body=pod)

    def parse_creat(self):
        data = json.load(open("file.json", "r"))
        for i in data:
            print(i["name"])
            # pod = client.V1Pod(labels={"app": i["name"]})
            pod = client.V1Pod()
            pod.metadata = client.V1ObjectMeta(name=str(i["name"] + "-" + str(time.time())))
            print(time.time())
            container = client.V1Container(image=i["name"], name=i["name"])
            spec = client.V1PodSpec(containers=[container])
            # spec.containers = [container]
            for node_name in i["nodes"]:
                spec.node_name = node_name
                pod.spec = spec
                self.core_v1.create_namespaced_pod(namespace="default", body=pod)

    def getPod(self):
        print('Listing pods with their IPs')
        ret = self.core_v1.list_pod_for_all_namespaces(watch=False)
        pod_list = []
        count = 0
        for i in ret.items:
            name = i.metadata.name
            namespace = i.metadata.namespace
            node = i.spec.node_name
            create_time = i.metadata.creation_timestamp
            phase = i.status.phase
            image = i.spec.containers[0].image
            pod_list.append({'name': name,
                             'namespace': namespace,
                             'node': node,
                             'create_time': create_time,
                             'phase': phase,
                             'image': image})
            # pod_list.append({'phase': phase})
            count += 1
        return {'pod_list': pod_list, 'num': count}

    def getNS(self):
        print('Listing NSs and return the number of NSs')
        ret = self.core_v1.list_namespace()
        for i in ret.items:
            print("%s\t%s" % (i.metadata.name, i.metadata.creation_timestamp))
        return {'dic': ret.items, 'num': len(ret.items)}

    def getService(self):
        print('List Services with their IPs and the number of services')
        ret = self.core_v1.list_service_for_all_namespaces()
        for i in ret.items:
            print("%s\t%s\t%s\t%s" % (
                i.spec.cluster_ip, i.metadata.namespace, i.metadata.name, i.metadata.creation_timestamp))
        return {'dic': ret.items, 'num': len(ret.items)}

    def getDeployment(self):
        print('List Deployments and the number of Deployments')
        ret = self.apps_v1.list_deployment_for_all_namespaces()
        # for i in ret.items:
        #     print("%s\t%s\t%s\t%s" % ())
        return {'dic': ret.items, 'num': len(ret.items)}
        pass

    def getService_2(self):
        print('Return Service list')
        ret = self.core_v1.list_service_for_all_namespaces()
        ret2 = self.core_v1.list_pod_for_all_namespaces()
        service_list = []
        count = 0

        for i in ret.items:
            # ip = i.status.load_balancer.ingress.ip
            # hostname = i.status.load_balancer.ingress.hostname
            # create_time = i.metadata.creation_timestamp
            # present_time = time.localtime(time.time())
            # lasting_time = time.strftime('%H:%M:%S', present_time - create_time)
            create_time = i.metadata.creation_timestamp.strftime('%Y-%m-%d %H:%M:%S')
            present_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            create_time = time.mktime(time.strptime(create_time, "%Y-%m-%d %H:%M:%S"))
            present_time = time.mktime(time.strptime(present_time, "%Y-%m-%d %H:%M:%S"))
            lasting_time = time.strftime('%H:%M:%S', time.localtime(present_time - create_time))
            # lasting_time = datetime.timedelta(present_time, create_time)
            cluster_ip = i.spec.cluster_ip
            selector_check = i.spec.selector
            name = i.metadata.name
            tag = i.metadata.labels
            port = str(str(i.spec.ports[0].port) + ":" + str(i.spec.ports[0].protocol))
            target_port = i.spec.ports[0].target_port
            running_status = "正常"

            for m in ret2.items:
                if m.metadata.labels == selector_check and (m.status.phase == "Failed" or m.status.phase == "Unknown"):
                    running_status = "异常"

            service_list.append({
                # 'ip': ip,
                # 'hostname': hostname,
                'time': lasting_time,
                'cluster_ip': cluster_ip,
                'name': name,
                'tag': tag,
                'port': port,
                'target_port': target_port,
                'running_status': running_status})
            count += 1
        return {'service_list': service_list, 'num': count}

    def getNode(self):
        print('Return the number of node')
        ret = self.core_v1.list_node()
        count = 0
        node_list = []
        capacity_cpu_sum = 0
        allocatable_cpu_sum = 0
        capacity_mem_sum = 0
        allocatable_mem_sum = 0
        for i in ret.items:
            ip = i.status.addresses[0].address
            name = i.status.addresses[1].address
            allocatable_cpu = int(i.status.allocatable['cpu'])
            allocatable_cpu_sum += allocatable_cpu
            allocatable_mem = int(i.status.allocatable['memory'][:-2]) / 1048576
            allocatable_mem_sum += allocatable_mem
            capacity_cpu = int(i.status.capacity['cpu'])
            capacity_cpu_sum += capacity_cpu
            capacity_mem = int(i.status.capacity['memory'][:-2]) / 1048576
            capacity_mem_sum += capacity_mem
            node_list.append({'ip': ip,
                              'name': name,
                              'allocatable_cpu': allocatable_cpu,
                              'allocatable_mem': int(allocatable_mem),
                              'capacity_cpu': capacity_cpu,
                              'capacity_mem': int(capacity_mem)})
            count += 1
        cpu_ratio = int((allocatable_cpu_sum / capacity_cpu_sum) * 100)
        mem_ratio = int((allocatable_mem_sum / capacity_mem_sum) * 100)
        return {'node_list': node_list, 'num': count, 'cpu_ratio': cpu_ratio, 'mem_ratio': mem_ratio}

    def createService(self, name, selector, service_port=None, namespace='default'):
        port = None
        if service_port is not None:
            port = [client.V1ServicePort(port=service_port)]
        spec = client.V1ServiceSpec(
            ports=port,
            selector=selector
        )
        service = client.V1Service(
            api_version='v1',
            kind='Service',
            metadata=client.V1ObjectMeta(name=name),
            spec=spec
        )
        response = self.core_v1.create_namespaced_service(
            body=service,
            namespace=namespace
        )
        print("Service created. status='%s'" % str(response.status))

    def createNamespace(self, name):
        namespace = client.V1Namespace(
            api_version='v1',
            kind='Namespace',
            metadata=client.V1ObjectMeta(name=name)
        )
        response = self.core_v1.create_namespace(body=namespace)
        print("Namespace created. status='%s" % str(response.status))
