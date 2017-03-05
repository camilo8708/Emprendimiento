#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from datetime import datetime
from django.http import HttpResponse
from componentes.models import Encuesta, Cliente, Empresa


def encuesta(request, id):
    data = {}
    if request.method == "GET":
        try:
            isAdmin = False
            encuesta = Encuesta.objects.get(id=id)
            cliente = Cliente.objects.get(id=encuesta.idCliente)
            empresa = Empresa.objects.get(id=cliente.idEmpresa)
            response_encuesta = []
            response_encuesta_tmp = {}
            response_encuesta_tmp['id'] = str(encuesta.id)
            response_encuesta_tmp['fechaEnvio'] = str(encuesta.fechaEnvio.strftime('%Y/%m/%d'))
            #response_encuesta_tmp['fechaRespuesta'] = str(encuesta.fechaRespuesta.strftime('%Y/%m/%d'))
            response_encuesta_tmp['preguntaExperiencia'] = encuesta.preguntaExperiencia
            response_encuesta_tmp['primerComentario'] = encuesta.primerComentario
            response_encuesta_tmp['SegundoComentario'] = encuesta.SegundoComentario
            response_encuesta_tmp['estadoEncuesta'] = encuesta.estadoEncuesta
            response_encuesta_tmp['primerNombre'] = cliente.primerNombre
            response_encuesta_tmp['otrosNombre'] = cliente.otrosNombre
            response_encuesta_tmp['primerApellido'] = cliente.primerApellido
            response_encuesta_tmp['segundoApellido'] = cliente.segundoApellido
            response_encuesta_tmp['logo'] = empresa.logo
            response_encuesta_tmp['nombreEmpresa'] = empresa.nombre

            response_encuesta.append(response_encuesta_tmp)


            return HttpResponse(json.dumps(response_encuesta), content_type='application/json; charset=UTF-8')

        except Exception as e:
            return HttpResponse(json.dumps(e.args), content_type="application/json", status=400)

    return HttpResponse(json.dumps(data), content_type='application/json; charset=UTF-8')
