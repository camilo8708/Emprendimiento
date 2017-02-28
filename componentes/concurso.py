#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import boto3
import os
import uuid
from django.http import HttpResponse
from django.core import serializers
from componentes.models import Concurso, Video, Empresa
from componentes.tasks import convertirVideo
from datetime import datetime

def concurso(request, url):
    data = {}
    if request.method == "GET":
        try:
            cf= os.environ.get('AWS_CLOUD_FRONT', '')
            isAdmin = False
            concurso = Concurso.objects.get(url=url)
            empresa = Empresa.objects.get(id=concurso.idEmpresa)
            if(request.GET['idAdmin'] == '' or request.GET['idAdmin'] != str(empresa.id)):
                isAdmin = False
                videos = Video.objects.filter(idConcurso=concurso.id, estado='Convertido').order_by('-fechaRegistro')
            else:
                videos = Video.objects.filter(idConcurso=concurso.id).order_by('-fechaRegistro')
                isAdmin = True

            response_videos = []
            for item in videos:
                response_video_tmp = {}
                response_video_tmp['id'] = str(item.id)
                response_video_tmp['idConcurso'] = str(item.idConcurso)
                response_video_tmp['video'] = str(item.video).replace('https://s3.amazonaws.com/smarttools-grupo7/',cf)
                response_video_tmp['videoMP4'] = str(item.videoMP4).replace('https://s3.amazonaws.com/smarttools-grupo7/',cf)
                response_video_tmp['estado'] = item.estado
                response_video_tmp['nombres'] = item.nombres
                response_video_tmp['apellidos'] = item.apellidos
                response_video_tmp['correoElectronico'] = item.correoElectronico
                response_video_tmp['descripcion'] = item.descripcion
                response_video_tmp['fechaRegistro'] = str(item.fechaRegistro)
                response_videos.append(response_video_tmp)

            # JSON
            data = {
                "videos": response_videos,
                "nombreConcurso": concurso.nombre,
                "foto": concurso.foto ,
                "fechaInicio": str(concurso.fechaInicio),
                "fechaFin": str(concurso.fechaFin),
                "descripcion": concurso.descripcion ,
                "creadoPor": empresa.nombres +' ' + empresa.apellidos,
                "isAdmin": isAdmin
            }
            return HttpResponse(json.dumps(data), content_type='application/json; charset=UTF-8')

        except Exception as e:
            return HttpResponse(json.dumps(e.args), content_type="application/json", status=400)

    if request.method == "POST":
        s3 = boto3.resource('s3',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID', ''),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY', ''))

        try:
            concurso = Concurso.objects.get(url=url)
            nombres = request.POST['nombres']
            apellidos = request.POST['apellidos']
            correoElectronico = request.POST['correoElectronico']
            desc = request.POST['desc']
            estado = "En proceso"
            if 'file' in request.FILES:
                my_uuid = uuid.uuid4()
                imgNombreOriginal = request.FILES['file'].name
                imgExt = imgNombreOriginal[(imgNombreOriginal.rfind('.')): len(imgNombreOriginal)].lower()
                video = 'https://s3.amazonaws.com/smarttools-grupo7/videos/' + str(concurso.url) + str(
                    my_uuid) + imgExt
                s3.Bucket('smarttools-grupo7').put_object(Key='videos/' + str(concurso.url) + str(my_uuid) + imgExt,
                                                          Body=request.FILES['file'])
            else:
                video = ''

            video_nuevo = Video(nombres=nombres, apellidos=apellidos, correoElectronico=correoElectronico, descripcion=desc,
                           estado=estado, video=video, idConcurso = concurso.id, fechaRegistro=datetime.now())
            video_nuevo.save()
            #Enviar Video a la Cola
            convertirVideo.delay(str(video_nuevo.id))
            return HttpResponse(video_nuevo.to_json(), content_type="application/json")

        except Exception as e:
            print e.message
            return HttpResponse(json.dumps(e.args), content_type="application/json", status=400)

    return HttpResponse(json.dumps(data), content_type='application/json; charset=UTF-8')


# Función encargada de retornar los concursos
def utilConcursoById(request, id):
    try:
        if request.method == 'DELETE':
            concurso = Concurso.objects.get(id=id)
            concurso.delete()
            return HttpResponse(json.dumps([]), content_type="application/json")
        if request.method == 'GET':
            response_data = {}
            concurso = Concurso.objects.get(id=id)
            empresa = Empresa.objects.get(id=concurso.idEmpresa)

            response_data['pk'] = str(concurso.pk)
            response_data['nombre'] = concurso.nombre
            response_data['foto'] = str(concurso.foto)
            response_data['url'] = concurso.url
            response_data['fechaRegistro'] = str(concurso.fechaRegistro.strftime('%Y/%m/%d'))
            response_data['fechaInicio'] = str(concurso.fechaInicio.strftime('%Y/%m/%d'))
            response_data['fechaFin'] = str(concurso.fechaFin.strftime('%Y/%m/%d'))
            response_data['descripcion'] = concurso.descripcion
            response_data['empresa'] = (empresa.nombres) + " " + (empresa.apellidos)

            return HttpResponse(json.dumps(response_data), content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps(e.args), content_type="application/json", status=400)


def queryConcursosByEmpresa(request, id):
    try:
        response_data = []
        response_data_temp = {}
        concursos = Concurso.objects.filter(idEmpresa=id)
        empresa = Empresa.objects.get(id=id)

        for item in concursos:
            response_data_temp['pk'] = str(item.pk)
            response_data_temp['nombre'] = item.nombre
            response_data_temp['foto'] = str(item.foto)
            response_data_temp['url'] = item.url
            response_data_temp['fechaRegistro']  = str(item.fechaRegistro.strftime('%Y/%m/%d'))
            response_data_temp['descripcion'] = item.nombre
            response_data_temp['empresa'] = (empresa.nombres) + " " +(empresa.apellidos)
            response_data.append(response_data_temp)
            response_data_temp = {}

        return HttpResponse(json.dumps(response_data), content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps(e.args), content_type="application/json", status=400)


def createConcurso(request):
    s3 = boto3.resource(
        's3',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID', ''),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY', ''))
    try:
        # Crear concurso
        if request.method == 'POST':

            nombre = request.POST['nombre']
            url = request.POST['url']
            fechaInicio = datetime.strptime(request.POST['fechaInicio'], '%Y-%m-%d')
            fechaFin = datetime.strptime(request.POST['fechaFin'], '%Y-%m-%d')
            descripcion = request.POST['descripcion']
            idEmpresa = request.POST['idEmpresa']
            concursoDuplicado = Concurso.objects.filter(url=url)
            empresa = Empresa.objects.get(id=idEmpresa)

            if concursoDuplicado and concursoDuplicado.count() > 0:
                return HttpResponse("Ya existe un concurso con la misma url.", status=400)
            else:

                if 'file' in request.FILES:
                    imgNombreOriginal = request.FILES['file'].name
                    imgExt = imgNombreOriginal[(imgNombreOriginal.rfind('.')): len(imgNombreOriginal)].lower()
                    foto = 'https://s3.amazonaws.com/smarttools-grupo7/img/' + str(url) + imgExt
                    s3.Bucket('smarttools-grupo7').put_object(Key='img/' + str(url)+ imgExt, Body=request.FILES['file'])
                else:
                    foto = ''

                concurso = Concurso(nombre=nombre, url=url, fechaInicio=fechaInicio, fechaFin=fechaFin, descripcion=descripcion, idEmpresa=empresa.id, foto=foto, fechaRegistro=datetime.now())
                concurso.save()
                return HttpResponse(concurso.to_json(), content_type="application/json")

    except Exception as e:
        print e.message
        return HttpResponse(json.dumps(e.args), content_type="application/json", status=400)


def updateConcurso(request):
    s3 = boto3.resource(
        's3',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID', ''),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY', ''))
    try:
        id = request.POST['id']
        nombre = request.POST['nombre']
        url = request.POST['url']
        fechaInicio = datetime.strptime(request.POST['fechaInicio'], '%Y-%m-%d')
        fechaFin = datetime.strptime(request.POST['fechaFin'], '%Y-%m-%d')
        descripcion = request.POST['descripcion']

        concurso = Concurso.objects(url=url).first()
        if concurso != None and str(concurso.id) != id:
                return HttpResponse("Ya existe un concurso con la misma url.", status=400)

        concurso = Concurso.objects.get(id=id)
        if concurso:
            if 'file' in request.FILES:
                imgNombreOriginal = request.FILES['file'].name
                imgExt = imgNombreOriginal[(imgNombreOriginal.rfind('.')): len(imgNombreOriginal)].lower()
                foto = 'https://s3.amazonaws.com/smarttools-grupo7/img/' + str(url) + imgExt
                s3.Bucket('smarttools-grupo7').put_object(Key='img/' + str(url) + imgExt, Body=request.FILES['file'])
            else:
                foto = ''
            concurso.nombre = nombre
            concurso.url = url
            concurso.fechaInicio = fechaInicio
            concurso.fechaFin = fechaFin
            concurso.descripcion = descripcion
            concurso.foto = foto
            concurso.save()
            return HttpResponse(serializers.serialize('json', []), content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps(e.args), content_type="application/json", status=400)
