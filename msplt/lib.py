import kubernetes.client
from kubernetes.client.rest import ApiException
from pprint import pprint
from kubernetes import client, config, watch

class manager(object):
    def __init__(self):
        config.load_kube_config('E:/pythonProject/test/resource/config')
        self.core_v1 = client.CoreV1Api()
        self.apps_v1 = client.AppsV1Api()

    def getPod(self):
        print('Listing pods with their IPs')
        ret = self.core_v1.list_pod_for_all_namespaces(watch=False)
        for i in ret.items:
            print("%s\t%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name, i.metadata.creation_timestamp))
        return {'dic': ret.items, 'num': len(ret.items)}

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
            print("%s\t%s\t%s\t%s" % (i.spec.cluster_ip, i.metadata.namespace, i.metadata.name, i.metadata.creation_timestamp))
        return {'dic': ret.items, 'num': len(ret.items)}

    def getDeployment(self):
        # TODO
        pass

    def getNode(self):
        print('Return the number of node')
        ret = self.core_v1.list_node()
        count = 0
        node_list = []
        for i in ret.items:
            ip = i.status.addresses[0].address
            name = i.status.addresses[1].address
            allocatable_cpu = i.status.allocatable['cpu']
            allocatable_mem = i.status.allocatable['memory']
            capacity_cpu = i.status.capacity['cpu']
            capacity_mem = i.status.capacity['memory']
            node_list.append({'ip': ip,
                              'name': name,
                              'allocatable_cpu': allocatable_cpu,
                              'allocatable_mem': allocatable_mem,
                              'capacity_cpu': capacity_cpu,
                              'capacity_mem': capacity_mem})
            count += 1
        return {'node_list': node_list, 'num': count}

    def createDeployment(self, name, image, namespace='default', container_port=None, replicas=1):
        port = None
        if container_port is not None:
            port = [client.V1ContainerPort(container_port=container_port)]
        container = client.V1Container(
            name=name,
            image=image,
            ports=port
        )
        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={'app': name}),
            spec=client.V1PodSpec(containers=[container])
        )
        spec = client.V1DeploymentSpec(
            replicas=replicas,
            template=template,
            selector={'matchLabels': {'app': name}}
        )
        deployment = client.V1Deployment(
            api_version='app/v1',
            kind='Deployment',
            metadata=client.V1ObjectMeta(name=name),
            spec=spec
        )
        response = self.apps_v1.create_namespaced_deployment(
            body=deployment,
            namespace=namespace)
        print("Deployment created. status='%s'" % str(response.status))

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

