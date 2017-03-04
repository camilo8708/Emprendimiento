from django.conf.urls import url

from componentes import concurso, empresa, encuesta
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^login_view/', views.login, name='login_view'),
    url(r'^post_login/', views.post_login, name='post_register'),
    url(r'^login/g/', views.get_session_data, name='get_session_data'),
    url(r'^login/c/', views.clear_session_data, name='clear_session_data'),
    url(r'^concurso/(?P<url>\w+)/$', concurso.concurso, name='concurso'),
    url(r'^encuesta/(?P<url>\w+)/$', encuesta.encuesta, name='encuesta'),
    url(r'^concursos/util/(?P<id>\w+)/$', concurso.utilConcursoById, name='concursoUtil'),
    url(r'^concursos/u/$', concurso.updateConcurso, name="updateConcurso"),
    url(r'^concursos/(?P<id>\w+)/$', concurso.queryConcursosByEmpresa, name='concurso'),
    url(r'^concursos/$', concurso.createConcurso, name="createConcurso"),
    url(r'^empresas/$', empresa.crearEmpresa, name='crearEmpresa'),
]
