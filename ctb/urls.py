from django.conf.urls import url
from . import views

app_name = 'ctb'

urlpatterns = [
    url(r'^$', views.ctb_index, name='ctb-index'),
    url(r'^list/(?P<empresa_id>[0-9]+)/$', views.conta_list, name='conta-list'),
    url(r'^create/$', views.conta_create, name='conta-add'),
    url(r'^detail/(?P<conta_id>[0-9]+)/$', views.conta_detail, name="conta-detalhe"),
    url(r'^update/$', views.conta_update),
    url(r'^delete/$', views.conta_delete),
    url(r'^wip/$', views.work_in_progress, name="wip")
]