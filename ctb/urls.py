from django.conf.urls import url

from ctb import views
from ctb.views import HistoricoList, HistoricoDetalhe, HistoricoCreate, HistoricoUpdate, historico_delete, \
    ContaList, ContaDetalhe, ContaCreate, ContaUpdate, conta_delete

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

    # WORK IN PROGRESS
    url(r'^wip/$', views.work_in_progress, name="wip"),

]
