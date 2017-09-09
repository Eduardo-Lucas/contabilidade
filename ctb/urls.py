from django.conf.urls import url

from ctb import views
from ctb.views import CompetenciaList, CompetenciaDetalhe, CompetenciaCreate, CompetenciaUpdate, competencia_delete, \
                      ContaList,       ContaDetalhe,       ContaCreate,       ContaUpdate,       conta_delete, \
                      EmpresaList,     EmpresaDetalhe,     EmpresaCreate,     EmpresaUpdate,     empresa_delete, \
                      HistoricoList,   HistoricoDetalhe,   HistoricoCreate,   HistoricoUpdate,   historico_delete

app_name = 'ctb'

urlpatterns = [
    url(r'^$', views.ctb_index, name='ctb-index'),

    # Contas
    url(r'^conta-list/$', ContaList.as_view(), name='conta-list'),
    url(r'^conta-list/(?P<pk>[0-9]+)/$', ContaDetalhe.as_view(), name="conta-detail"),
    url(r'^conta-add/$', ContaCreate.as_view(), name='conta-add'),
    url(r'^conta/(?P<pk>[0-9]+)/edit/$', ContaUpdate.as_view(), name='conta-edit'),
    url(r'^conta/(?P<id>[0-9]+)/delete/$', conta_delete, name='conta-delete'),

    # Historicos
    url(r'^historico-list/$', HistoricoList.as_view(), name='historico-list'),
    url(r'^historico-list/(?P<pk>[0-9]+)/$', HistoricoDetalhe.as_view(), name='historico-detail'),
    url(r'^historico-add/$', HistoricoCreate.as_view(), name='historico-add'),
    url(r'^historico/(?P<pk>[0-9]+)/edit/$', HistoricoUpdate.as_view(), name='historico-edit'),
    url(r'^historico/(?P<id>[0-9]+)/delete/$', historico_delete, name='historico-delete'),

    # Empresas
    url(r'^empresa-list/$', EmpresaList.as_view(), name='empresa-list'),
    url(r'^empresa-list/(?P<pk>[0-9]+)/$', EmpresaDetalhe.as_view(), name="empresa-detail"),
    url(r'^empresa-add/$', EmpresaCreate.as_view(), name='empresa-add'),
    url(r'^empresa/(?P<pk>[0-9]+)/edit/$', EmpresaUpdate.as_view(), name='empresa-edit'),
    url(r'^empresa/(?P<id>[0-9]+)/delete/$', empresa_delete, name='empresa-delete'),

    # Competências
    url(r'^competencia-list/$', CompetenciaList.as_view(), name='competencia-list'),
    url(r'^competencia-list/(?P<pk>[0-9]+)/$', CompetenciaDetalhe.as_view(), name='competencia-detail'),
    url(r'^competencia-add/$', CompetenciaCreate.as_view(), name='competencia-add'),
    url(r'^competencia/(?P<pk>[0-9]+)/edit/$', CompetenciaUpdate.as_view(), name='competencia-edit'),
    url(r'^competencia/(?P<id>[0-9]+)/delete/$', competencia_delete, name='competencia-delete'),

    # WORK IN PROGRESS
    url(r'^wip/$', views.work_in_progress, name="wip"),

]
