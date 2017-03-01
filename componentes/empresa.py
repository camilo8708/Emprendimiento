#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from datetime import datetime
from django.http import HttpResponse

from componentes.empleado import *
from .models import Empresa


def crearEmpresa(request):
    try:
        if request.method == 'POST':
            nombres = request.POST['nombres']
            apellidos = request.POST['apellidos']
            correoElectronico = request.POST['correoElectronico']
            telefono = request.POST['telefono']
            contrasenia = request.POST['contrasenia']
            nombreEmpresa = request.POST['nombreEmpresa']

            empresas = Empresa.objects.filter(nombre=nombreEmpresa)

            if len(empresas) > 0:
                return HttpResponse("Otra Empresa ya se ha registrado con el mismo correo electrónico.",
                                    status=400)

            if(existeEmpleado(correoElectronico)):
                return HttpResponse("Otro Usuario ya se ha registrado con el mismo correo electrónico.",
                                    status=400)

            empresa_nueva = Empresa(nombre=nombreEmpresa, fechaRegistro=datetime.now())
            empresa_nueva.save()

            crearEmpleado(nombres, apellidos, correoElectronico, telefono, contrasenia, "Admin", empresa_nueva.id)

            return HttpResponse(empresa_nueva.to_json(), content_type="application/json")

    except Exception as e:
        print e
        return HttpResponse(json.dumps(e.args), content_type="application/json", status=400)
