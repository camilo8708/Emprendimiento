from __future__ import unicode_literals

from datetime import datetime
from mongoengine import *

# Cristian Huertas - 08-10-16:/Modelo Proyecto Smarttools

class Video(Document):
    idConcurso = ObjectIdField()
    video = StringField()
    videoMP4 = StringField()
    estado = StringField(max_length=30)
    nombres = StringField(max_length=50)
    apellidos = StringField(max_length=50)
    correoElectronico = EmailField(max_length=50)
    descripcion = StringField(max_length=1000)
    fechaRegistro = DateTimeField()


class Concurso(Document):
    idEmpresa = ObjectIdField()
    nombre = StringField(max_length=100)
    foto = StringField()
    url = StringField(max_length=30, unique=True)
    fechaRegistro = DateTimeField()
    fechaInicio = DateTimeField()
    fechaFin = DateTimeField()
    descripcion = StringField(max_length=1000)


class Empresa(Document):
    nombres = StringField(max_length=50)
    apellidos = StringField(max_length=50)
    correoElectronico = EmailField(max_length=50, unique=True)
    contrasenia = StringField(max_length=15)
    tipo = StringField(max_length=15)
    fechaRegistro = DateTimeField()