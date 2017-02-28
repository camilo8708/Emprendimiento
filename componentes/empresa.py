#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from datetime import datetime
from django.http import HttpResponse
from .models import Empresa


def crearEmpresa(request):
    try:
        if request.method == 'POST':
            nombres = request.POST['nombres']
            apellidos = request.POST['apellidos']
            correoElectronico = request.POST['correoElectronico']
            contrasenia = request.POST['contrasenia']
            tipo = 'Empresa'

            empresas = Empresa.objects.filter(correoElectronico=correoElectronico, tipo=tipo)

            if len(empresas) > 0:
                return HttpResponse("Otra Empresa ya se ha registrado con el mismo correo electrónico.",
                                    status=400)

            empresa_nueva = Empresa(nombres=nombres, apellidos=apellidos, correoElectronico=correoElectronico,contrasenia=contrasenia, tipo=tipo, fechaRegistro=datetime.now())
            empresa_nueva.save()
            return HttpResponse(empresa_nueva.to_json(), content_type="application/json")

    except Exception as e:
        print e
        return HttpResponse(json.dumps(e.args), content_type="application/json", status=400)



