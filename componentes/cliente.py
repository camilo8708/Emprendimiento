#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os

from datetime import datetime
from componentes.tasks import enviarEncuesta

import boto3
from django.http import HttpResponse

from .models import Empresa, Cliente, Empleado


def crearCliente(request):
    try:
        if request.method == 'POST':
            nombre1 = request.POST['nombre1']
            nombre2 = request.POST['nombre2']
            apellido1 = request.POST['apellido1']
            apellido2 = request.POST['apellido2']
            correo = request.POST['correo']
            tipoIdenti = request.POST['tipoIdenti']
            identi = request.POST['identi']
            telefono1 = request.POST['telefono1']
            telefono2 = request.POST['telefono2']
            celular = request.POST['celular']
            idEmpleado = request.POST['idEmpleado']

            #consultar empresa logueada
            empleado = Empleado.objects.get(id=idEmpleado)

            #Creacion cliente
            cliente = Cliente(correoElectronico=correo, primerNombre=nombre1, otrosNombre=nombre2, primerApellido=apellido1,
                              segundoApellido=apellido2, tipoIdentificacion=tipoIdenti, numeroIdentificacion=identi,
                              telefonoPrincipal=telefono1, telefonoSecundario=telefono2, celular=celular, idEmpresa=empleado.idEmpresa)
            cliente.save()

            #Enviar Cliente a la Cola
            enviarEncuesta.delay(str(cliente.id))

            return HttpResponse(cliente.to_json(), content_type="application/json")

    except Exception as e:
        print e
        return HttpResponse(json.dumps(e.args), content_type="application/json", status=400)
