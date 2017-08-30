from django.conf.urls import url

from ctb import views
from ctb.views import HistoricoList, HistoricoDetalhe, HistoricoCreate, HistoricoUpdate, HistoricoDelete, ContaList, \
    ContaDetalhe, ContaCreate, ContaUpdate,  ContaDelete

app_name = 'ctb'

urlpatterns = [
    url(r'^$', views.ctb_index, name='ctb-index'),
    url(r'^conta-list/$', ContaList.as_view(), name='conta-list'),
    url(r'^conta-list/(?P<pk>[0-9]+)/$', ContaDetalhe.as_view(), name="conta-detail"),
    url(r'^conta-add/$', ContaCreate.as_view(), name='conta-add'),
    url(r'^conta/(?P<pk>[0-9]+)/edit/$', ContaUpdate.as_view(), name='conta-edit'),
    url(r'^conta/(?P<pk>[0-9]+)/delete/$', ContaDelete.as_view(), name='conta-delete'),

    # Historicos
    url(r'^historico-list/$', HistoricoList.as_view(), name='historico-list'),
    url(r'^historico-list/(?P<pk>[0-9]+)/$', HistoricoDetalhe.as_view(), name='historico-detail'),
    url(r'^historico-add/$', HistoricoCreate.as_view(), name='historico-add'),
    url(r'^historico-edit/(?P<pk>[0-9]+)/$', HistoricoUpdate.as_view(), name='historico-edit'),
    url(r'^historico-delete/(?P<pk>[0-9]+)/$', HistoricoDelete.as_view(), name='historico-delete'),

    # WORK IN PROGRESS
    url(r'^wip/$', views.work_in_progress, name="wip"),

]
