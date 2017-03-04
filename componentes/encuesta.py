#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse

from componentes.models import Encuesta


def encuesta(request, url):
    data = {}
    if request.method == "GET":
        try:
            isAdmin = False
            encuesta = Encuesta.objects.get(id=url)
            
            response_encuesta = []
            for item in encuesta:
                response_encuesta_tmp = {}
                response_encuesta_tmp['id'] = str(item.id)
                response_encuesta_tmp['fechaEnvio'] = str(item.fechaEnvio.strftime('%Y/%m/%d'))
                response_encuesta_tmp['fechaRespuesta'] = str(item.fechaRespuesta.strftime('%Y/%m/%d'))
                response_encuesta_tmp['preguntaExperiencia'] = item.preguntaExperiencia
                response_encuesta_tmp['primerComentario'] = item.primerComentario
                response_encuesta_tmp['SegundoComentario'] = item.SegundoComentario
                response_encuesta_tmp['estadoEncuesta'] = item.estadoEncuesta
                response_encuesta_tmp['primerNombre'] = item.idCliente.primerNombre
                response_encuesta_tmp['otrosNombre'] = item.idCliente.otrosNombre
                response_encuesta_tmp['primerApellido'] = item.idCliente.primerApellido
                response_encuesta_tmp['segundoApellido'] = item.idCliente.segundoApellido
                response_encuesta_tmp['logo'] = item.idCliente.idEmpresa.logo
                response_encuesta_tmp['nombreEmpresa'] = item.idCliente.idEmpresa.nombre

                response_encuesta.append(response_encuesta_tmp)


            return HttpResponse(json.dumps(response_encuesta), content_type='application/json; charset=UTF-8')

        except Exception as e:
            return HttpResponse(json.dumps(e.args), content_type="application/json", status=400)

    return HttpResponse(json.dumps(data), content_type='application/json; charset=UTF-8')
