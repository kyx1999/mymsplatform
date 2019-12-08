#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import threading
import time

from django.http import request
from kubernetes import client, config
from django.contrib import messages
from django.shortcuts import redirect


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mymsplatform.settings')
    try:
        from django.core.management import execute_from_command_line

    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        )(exc)
    execute_from_command_line(sys.argv)


# def create_thread(request):
#     while True:
#         config.load_kube_config('~/.kube/config')
#         v1 = client.CoreV1Api()
#         pod_list = v1.list_pod_for_all_namespaces()
#         for i in pod_list.items:
#             if i.status.phase == "Failed" or i.status.phase == "Unknown" or i.status.phase == "Pending":
#                 print(i.status.phase)
#                 # messages.add_message(request, messages.INFO, 'Hello world.')
#                 # messages.warning(request="有任务处于异常！")
#                 messages.success(request, "有任务处于异常！")
#                 return redirect('/index.html')


if __name__ == '__main__':
    # t = threading.Thread(target=create_thread)
    # t.start()
    main()
