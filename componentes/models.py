from __future__ import unicode_literals

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


#class Empresa(Document):
#    nombres = StringField(max_length=50)
#    apellidos = StringField(max_length=50)
#    correoElectronico = EmailField(max_length=50, unique=True)
#    contrasenia = StringField(max_length=15)
#    tipo = StringField(max_length=15)
#    fechaRegistro = DateTimeField()

# Cristian Huertas - 27-02-17:/Modelo Proyecto Emprendimiento
class Empresa(Document):
    nombre = StringField(max_length=200)
    fechaRegistro = DateTimeField()
    logo = StringField()

class Empleado(Document):
    correoElectronico = EmailField(max_length=50, unique=True)
    contrasenia = StringField(max_length=20)
    nombre = StringField(max_length=50)
    apellido = StringField(max_length=50)
    tipo = StringField(max_length=20)
    telefono = IntField(min_value=0)
    fechaRegistro = DateTimeField()
    idEmpresa = ObjectIdField()

class Cliente(Document):
    correoElectronico = EmailField(max_length=50)
    primerNombre = StringField(max_length=50)
    otrosNombre = StringField(max_length=50)
    primerApellido = StringField(max_length=50)
    segundoApellido = StringField(max_length=50)
    tipoIdentificacion = StringField(max_length=20)
    numeroIdentificacion = StringField(max_length=10)
    telefonoPrincipal = StringField(max_length=20)
    telefonoSecundario = StringField(max_length=20)
    celular = StringField(max_length=20)
    idEmpresa = ObjectIdField()

class Encuesta(Document):
    fechaEnvio = DateTimeField()
    fechaRespuesta = DateTimeField()
    preguntaRecomendacion = IntField(min_value=0, max_value=10)
    preguntaExperiencia = IntField(min_value=1, max_value=5)
    primerComentario = StringField(max_length=1000)
    SegundoComentario = StringField(max_length=1000)
    estadoEncuesta = StringField(max_length=1000)
    idCliente = ObjectIdField()

class tipoId(Document):
    nombre = StringField(max_length=20)
    acronimo = StringField(max_length=2)

class Parametro(Document):
    seq = IntField(unique=True)
    valor = StringField(max_length=14000)