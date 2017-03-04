#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os

from datetime import datetime

import boto3
from django.http import HttpResponse

from componentes.empleado import *
from .models import Empresa


def crearEmpresa(request):
    s3 = boto3.resource(
        's3',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID', ''),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY', ''))
    try:
        if request.method == 'POST':
            nombres = request.POST['nombres']
            apellidos = request.POST['apellidos']
            correoElectronico = request.POST['correoElectronico'].lower()
            telefono = request.POST['telefono']
            contrasenia = request.POST['contrasenia']
            nombreEmpresa = request.POST['nombreEmpresa'].upper()

            empresas = Empresa.objects.filter(nombre=nombreEmpresa)

            if len(empresas) > 0:
                return HttpResponse("La empresa ya se encuentra registrada.",
                                    status=400)

            if(existeEmpleado(correoElectronico)):
                return HttpResponse("Otro Usuario ya se ha registrado con el mismo correo electrónico.",
                                    status=400)

            if 'file' in request.FILES:
                imgNombreOriginal = request.FILES['file'].name
                imgExt = imgNombreOriginal[(imgNombreOriginal.rfind('.')): len(imgNombreOriginal)].lower()
                foto = 'https://s3.amazonaws.com/emprendimiento-grupo6/img/' + str(nombreEmpresa) + imgExt
                s3.Bucket('emprendimiento-grupo6').put_object(Key='img/' + str(nombreEmpresa)+ imgExt, Body=request.FILES['file'])
            else:
                foto = ''

            empresa_nueva = Empresa(nombre=nombreEmpresa, fechaRegistro=datetime.now(), logo = foto)
            empresa_nueva.save()

            crearEmpleado(nombres, apellidos, correoElectronico, telefono, contrasenia, "Admin", empresa_nueva.id)

            return HttpResponse(empresa_nueva.to_json(), content_type="application/json")

    except Exception as e:
        print e
        return HttpResponse(json.dumps(e.args), content_type="application/json", status=400)
