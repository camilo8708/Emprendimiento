import os
import subprocess

import boto3
from django.core.files import File
from datetime import datetime

from componentes.models import Video, Concurso, Cliente, Empresa, Parametro, Encuesta
from smarttools.celery import app


@app.task(ignore_result=True)
def enviarEncuesta(idCliente):
    # Se carga la infromacion necesaria para el mensaje
    cliente = Cliente.objects.get(id=idCliente)
    empresa = Empresa.objects.get(id=cliente.idEmpresa)

    # Se crea la encuesta para el cliente
    encuesta = Encuesta(fechaEnvio=datetime.now(), estadoEncuesta='Pendiente', idCliente=cliente.id)
    encuesta.save()

    # Se envia email de confirmacion
    parametro = Parametro.objects.get(seq=1)
    to = cliente.correoElectronico
    asunto = 'Encuesta de ' + empresa.nombre.title()
    mensaje = parametro.valor
    mensaje = mensaje.replace('^', '"')
    mensaje = mensaje.replace('**ruta_logo_empresa**', empresa.logo)
    mensaje = mensaje.replace('**nombre_cliente**', cliente.primerNombre.title() + ' ' + cliente.primerApellido.title())
    mensaje = mensaje.replace('**nombre_empresa**', empresa.nombre.title())
    mensaje = mensaje.replace('**url_encuesta**', 'https://cx-col.herokuapp.com/#/encuesta/'+str(encuesta.id))
    from componentes.mail import Mail
    mail = Mail(to, asunto, mensaje)
    mail.send()


@app.task(ignore_result=True)
def convertirVideo(idVideo):
    s3 = boto3.resource(
        's3',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID', ''),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY', ''))
    try:
        # Se define la ruta y formato destino
        video = Video.objects.get(id=idVideo)
        video_name = str(video.video).replace('https://s3.amazonaws.com/smarttools-grupo7/videos/','')
        video_ruta=download(video_name)
        destino = 'con_'+ video_name.rstrip()[0:len(video_name.rstrip()) - 3] + 'mp4'
        # Se jecuta el proceso de conversion de video
        executeCommand('ffmpeg -i ' + video_ruta + ' -acodec aac -vcodec libx264 ' + 'smarttools/static/media/videos/'+destino)
        f = open('smarttools/static/media/videos/'+destino, 'rb')
        if f :
            s3.Bucket('smarttools-grupo7').put_object(Key='videos/' + destino, Body=f)
            video.estado = 'Convertido'
            video.videoMP4 = 'https://s3.amazonaws.com/smarttools-grupo7/videos/'+destino
            video.save()
            f.close()
            # Se envia email de confirmacion
            concurso = Concurso.objects.get(id=video.idConcurso)
            to = video.correoElectronico
            asunto = 'Publicacion de video en el concurso ' + concurso.nombre
            mensaje = 'Su video ya se encuentra publicado en el concurso ' + concurso.nombre
            from componentes.mail import Mail
            mail = Mail(to, asunto, mensaje)
            mail.send()
            #Eliminar los videos temporales
            executeCommand('rm ' + 'smarttools/static/media/videos/'+video_name)
            executeCommand('rm ' + 'smarttools/static/media/videos/'+destino)
        else:
            video = ''
    except Exception as e:
        print('Error: ' + e.message)


def download(video_name):
    s3 = boto3.resource(
        's3',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID', ''),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY', ''))
    try:
        s3Bucket = s3.Bucket('smarttools-grupo7')
        s3Bucket.download_file('videos/'+video_name, 'smarttools/static/media/videos/'+video_name)
        return ('smarttools/static/media/videos/'+video_name)
    except Exception as e:
        print('Error: ' + e.message)

def executeCommand(command):
    if os.environ.get('LINUX', '') == 'TRUE':
        os.system(command)
    else:
        subprocess.call(command)
