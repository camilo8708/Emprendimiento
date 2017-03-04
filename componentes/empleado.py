#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from componentes.models import Empleado


def existeEmpleado(email):
    empleado = Empleado.objects.filter(correoElectronico=email)
    if len(empleado) > 0:
        return True
    return False

def crearEmpleado(nombres, apellidos, correoElectronico, telefono, contrasenia, rol, idEmpresa):
    empleado = Empleado(nombre=nombres, apellido=apellidos, correoElectronico=correoElectronico, tipo=rol, telefono=telefono, fechaRegistro=datetime.now(), idEmpresa=idEmpresa, contrasenia=contrasenia)
    empleado.save()



