from django.conf.urls import url

from ctb import views
from ctb.views import CompetenciaList, CompetenciaDetalhe, CompetenciaCreate, CompetenciaUpdate, competencia_delete, \
    ContaList, ContaDetalhe, ContaCreate, ContaUpdate, conta_delete, \
    EmpresaList, EmpresaDetalhe, EmpresaCreate, EmpresaUpdate, empresa_delete, \
    HistoricoList, HistoricoDetalhe, HistoricoCreate, HistoricoUpdate, historico_delete, MovimentoContabilHeaderList, \
    MovimentoContabilHeaderCreate, MovimentoContabilHeaderUpdate, movimento_contabil_header_delete, \
    MovimentoContabilHeaderDetalhe, SaldoContaContabilList, SaldoDetalhe, RazaoContabilList, LancamentoContabilCreate

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

    # FORMSET: Lancamento Contabil
    url(r'^lanc-add/$', LancamentoContabilCreate.as_view(), name='lanc-add'),


    # Movimentos Header
    url(r'^movimento-list/$', MovimentoContabilHeaderList.as_view(), name='movimento-list'),
    url(r'^movimento-detalhe/(?P<pk>[0-9]+)/$', MovimentoContabilHeaderDetalhe.as_view(), name='movimento-detail'),
    url(r'^movimento-add/$', MovimentoContabilHeaderCreate.as_view(), name='movimento-add'),
    url(r'^movimento/(?P<pk>[0-9]+)/edit/$', MovimentoContabilHeaderUpdate.as_view(), name='movimento-edit'),
    url(r'^movimento/(?P<id>[0-9]+)/delete/$', movimento_contabil_header_delete, name='movimento-delete'),

    # Lançamentos
    url(r'^(?P<movimentocontabilheader_id>[0-9]+)/create_lancamento/$', views.create_lancamento,
        name='lancamento-add'),
    url(r'^(?P<movimentocontabilheader_id>[0-9]+)/delete_lancamento/(?P<lancamentocontabil_id>[0-9]+)/$',
        views.delete_lancamento, name='lancamento-delete'),
    url(r'^razao_contabil/$', RazaoContabilList.as_view(), name='razao_contabil'),

    # saldo
    url(r'^saldo-lista/$', SaldoContaContabilList.as_view(), name='saldo-list'),
    url(r'^saldo-detalhe/(?P<pk>[0-9]+)/$', SaldoDetalhe.as_view(), name='saldo-detail'),

    # WORK IN PROGRESS
    url(r'^wip/$', views.work_in_progress, name="wip"),

]
