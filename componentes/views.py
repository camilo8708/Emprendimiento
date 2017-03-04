#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os, sys
from django.http import HttpResponse
from django.shortcuts import render
from .models import Empleado
from django.conf import settings
# Create your views here.
from iron_cache import *
# Método encargado de renderizar la página de inicio del proyecto.
from django.views.decorators.csrf import csrf_exempt
#from elasticache_pyclient import MemcacheClient

def index(request):
    return render(request, "componentes/index.html")


# Despliega la vista para el inicio de sesión
def login(request):
    return render(request, 'componentes/login.html')


@csrf_exempt
def post_login(request):
    try:
        ip = get_client_ip(request)
        empleado = Empleado.objects.get(correoElectronico=request.POST['correoElectronico'].lower())
        datos = {'id': str(empleado.id), 'rol': empleado.tipo}
        if (empleado.contrasenia == request.POST['contrasenia']):
                cache = IronCache()
                cache.name= 'Smarttools'
                item = cache.put(key=ip, value=json.dumps(datos))
                return HttpResponse(json.dumps(datos), content_type="application/json", status=200)
        else:
            return HttpResponse(json.dumps(empleado.correoElectronico + " " + empleado.contrasenia),
                                content_type="application/json", status=401)
    except Exception as e:
        print(e.message)
        return HttpResponse(json.dumps(e.args), content_type="application/json", status=400)


def get_session_data(request):
    try:

         ip = get_client_ip(request)
         #ip= (str(request.path).split('/'))[3]
         cache = IronCache()
         cache.name= 'Smarttools'
         datos=  json.loads(str(cache.get(key=ip)))
         return HttpResponse(json.dumps(datos), content_type="application/json", status=200)
    except Exception as e:
        print(e.message)
        return HttpResponse(json.dumps(e.args), content_type="application/json", status=400)

def clear_session_data(request):
    try:
         datos ={}
         #ip= (str(request.path).split('/'))[3]
         ip = get_client_ip(request)
         cache = IronCache()
         cache.name= 'Smarttools'
         datos= cache.delete(key=ip)
         return HttpResponse(json.dumps(datos), content_type="application/json", status=200)
    except Exception as e:
        print(e.message)
        return HttpResponse(json.dumps(e.args), content_type="application/json", status=400)




# Devuelve al mensaje json si el login fue exitoso (movil)
def generateLoginSuccesfulJSON(username):
    login_ok_json = {}
    login_ok_json['username'] = username
    login_ok_json['status'] = 'OK'
    login_ok_json['message'] = 'El usuario ha iniciado sesión'
    return login_ok_json


# Devuelve al mensaje json si el login fue fallido (movil)
def generateLoginFailedJSON(username):
    login_fail_json = {}
    login_fail_json['username'] = username
    login_fail_json['status'] = 'ERROR'
    login_fail_json['message'] = 'Usuario o Clave incorrecta'
    return login_fail_json


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip