import os
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse

from . import database
from .models import LabConsole 

import openstack

def _connect():
    server = os.getenv('OS_AUTH')
    project = os.getenv('OS_PROJECT_NAME')
    username = os.getenv('OS_USERNAME')
    password = os.getenv('OS_PASSWORD')
    return openstack.connection.Connection(
                auth=dict(
                auth_url=server,
                project_name=project,
                username=username,
                password=password,
                project_domain_name="Default",
                user_domain_name="Default"),
                identity_api_version=3,
                region_name="regionOne",
            )


def index(request):
    conn = _connect()
    return HttpResponse([server.name for server in conn.compute.servers()])
    #return render(request, 'welcome/index.html', {
    #    'hostname': hostname,
    #    'database': database.info(),
    #    'count': PageView.objects.count()
    #})

def console(request, server):
    conn = _connect()
    console = conn.compute.get_vnc_console(server)
    return HttpResponse(console)


def health(request):
    return HttpResponse(1)
