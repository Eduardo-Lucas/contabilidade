from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import transaction
from django.db.models import Sum, Q, Max
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView

from ctb.forms import ContaForm, LancamentoContabilForm, LancamentoContabilFormSet, MovimentoContabilHeaderForm
from ctb.models import Conta, Historico, Empresa, Competencia, MovimentoContabilHeader, LancamentoContabil, \
    SaldoContaContabil

"""
    PÁGINA PRINCIPAL DA CONTABILIDADE
"""


def index(request):
    context = {
                'title': 'Menu Principal',
                'current_user': request.user,
    }

    return render(request, "index.html", context)


@login_required()
def home(request):
    context = {
        'title': 'Home',
        'current_user': request.user,
    }

    return render(request, "home.html", context)




"""
       PLANO DE CONTAS
"""


class ContaList(SuccessMessageMixin, LoginRequiredMixin, ListView):
    model = Conta
    template_name = "ctb/conta/conta-list.html"

    def get_queryset(self):
        valor = self.request.GET.get('q')
        if valor:
            object_list = self.model.objects.filter(
                Q(codigo_conta__startswith=valor) |
                Q(codigo_conta__icontains=valor) |
                Q(conta__conta_superior__contains=valor) |
                Q(descricao__contains=valor.upper()) |
                Q(descricao__icontains=valor.title()) |
                Q(origem__icontains=valor) |
                Q(natureza__icontains=valor)
            )
        else:
            object_list = self.model.objects.all()

        paginator = Paginator(object_list, 10)  # Show 10 contas per page

        page = self.request.GET.get('page')
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            queryset = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            queryset = paginator.page(paginator.num_pages)

        # return object_list
        return queryset


class ContaDetalhe(SuccessMessageMixin, LoginRequiredMixin, DetailView):
    model = Conta
    template_name = "ctb/conta/conta_detail.html"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            calculated_field=self.object.descricao,
        )


class ContaCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Conta
    form_class = ContaForm
    success_message = '%(descricao)s criado com sucesso!'
    template_name = "ctb/conta/conta_form.html"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            calculated_field=self.object.descricao,
        )


class ContaUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Conta
    fields = '__all__'
    success_message = '%(descricao)s alterado com sucesso!'
    template_name = "ctb/conta/conta_form.html"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            calculated_field=self.object.descricao,
        )


def conta_delete(request, id=None):
    obj = get_object_or_404(Conta, id=id)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Registro apagado com sucesso!')
        return redirect('ctb:conta-list')

    context = {
        'object': obj
    }

    return render(request, 'ctb/confirm_delete.html', context)


"""
    WORK IN PROGRESS
"""


def work_in_progress(request):
    return render(request, "wip.html", {})

"""
    Historico - GENERIC VIEWS
"""


class HistoricoList(SuccessMessageMixin, LoginRequiredMixin, ListView):
    model = Historico
    template_name = 'ctb/historico/historico-list.html'

    def get_queryset(self):
        descricao = self.request.GET.get('q')
        if descricao:
            object_list = self.model.objects.filter(descricao__icontains=descricao)
        else:
            object_list = self.model.objects.all()

        paginator = Paginator(object_list, 9)  # Show 9 contas per page

        page = self.request.GET.get('page')
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            queryset = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            queryset = paginator.page(paginator.num_pages)

        # return object_list
        return queryset


class HistoricoDetalhe(SuccessMessageMixin, LoginRequiredMixin, DetailView):
    model = Historico
    template_name = 'ctb/historico/historico_detail.html'


class HistoricoCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Historico
    fields = '__all__'
    success_message = '%(descricao)s criado com sucesso!'
    template_name = "ctb/historico/historico_form.html"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            calculated_field=self.object.descricao,
        )


class HistoricoUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Historico
    fields = '__all__'
    success_message = '%(descricao)s alterado com sucesso!'
    template_name = 'ctb/historico/historico_form.html'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            calculated_field=self.object.descricao,
        )


def historico_delete(request, id=None):
    obj = get_object_or_404(Historico, id=id)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Registro apagado com sucesso!')
        return redirect('ctb:historico-list')

    context = {
        'object': obj
    }

    return render(request, 'ctb/confirm_delete.html', context)

"""
       EMPRESA
"""


class EmpresaList(SuccessMessageMixin, LoginRequiredMixin, ListView):
    model = Empresa
    template_name = "ctb/empresa/empresa-list.html"

    def get_queryset(self):
        razao_social = self.request.GET.get('q')
        if razao_social:
            object_list = self.model.objects.filter(razao_social__icontains=razao_social)
        else:
            object_list = self.model.objects.all()

        paginator = Paginator(object_list, 9)  # Show 10 contas per page

        page = self.request.GET.get('page')
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            queryset = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            queryset = paginator.page(paginator.num_pages)

        # return object_list
        return queryset


class EmpresaDetalhe(SuccessMessageMixin, LoginRequiredMixin, DetailView):
    model = Empresa
    success_message = 'Detalhe registro apresentado com sucesso!'
    template_name = "ctb/empresa/empresa_detail.html"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            calculated_field=self.object.razao_social,
        )


class EmpresaCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Empresa
    fields = '__all__'
    success_message = '%(razao_social)s criado com sucesso!'
    template_name = "ctb/empresa/empresa_form.html"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            calculated_field=self.object.razao_social,
        )


class EmpresaUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Empresa
    fields = '__all__'
    success_message = '%(razao_social)s alterado com sucesso!'
    template_name = "ctb/empresa/empresa_form.html"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            calculated_field=self.object.razao_social,
        )


def empresa_delete(request, id=None):
    obj = get_object_or_404(Empresa, id=id)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Registro apagado com sucesso!')
        return redirect('ctb:empresa-list')

    context = {
        'object': obj
    }

    return render(request, 'ctb/confirm_delete.html', context)


"""
    Competencia - GENERIC VIEWS
"""


class CompetenciaList(SuccessMessageMixin, LoginRequiredMixin, ListView):
    model = Competencia
    template_name = 'ctb/competencia/competencia-list.html'

    def get_queryset(self):
        data_competencia = self.request.GET.get('q')
        if data_competencia:
            object_list = self.model.objects.filter(data_competencia__icontains=data_competencia)
        else:
            object_list = self.model.objects.all()

        paginator = Paginator(object_list, 10)  # Show 10 contas per page

        page = self.request.GET.get('page')
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            queryset = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            queryset = paginator.page(paginator.num_pages)

        # return object_list
        return queryset


class CompetenciaDetalhe(SuccessMessageMixin, LoginRequiredMixin, DetailView):
    model = Competencia
    template_name = 'ctb/competencia/competencia_detail.html'


class CompetenciaCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Competencia
    fields = '__all__'
    success_message = '%(data_competencia)s criado com sucesso!'
    template_name = "ctb/competencia/competencia_form.html"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            calculated_field=self.object.data_competencia,
        )


class CompetenciaUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Competencia
    fields = '__all__'
    success_message = '%(data_competencia)s alterado com sucesso!'
    template_name = 'ctb/competencia/competencia_form.html'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            calculated_field=self.object.data_competencia,
        )


def competencia_delete(request, id=None):
    obj = get_object_or_404(Competencia, id=id)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Registro apagado com sucesso!')
        return redirect('ctb:competencia-list')

    context = {
        'object': obj
    }

    return render(request, 'ctb/confirm_delete.html', context)


"""
    Movimentos Contabeis HEADER - GENERIC VIEWS
"""


class MovimentoContabilHeaderList(SuccessMessageMixin, LoginRequiredMixin, ListView):
    model = MovimentoContabilHeader
    context_object_name = 'movimentocontabilheader'
    template_name = 'ctb/movimento_contabil_header/movimento_contabil_header-list.html'

    def get_queryset(self):
        valor = self.request.GET.get('q')
        if valor:
            object_list = self.model.objects.filter(
                Q(total_debito__icontains=valor) |
                Q(total_credito__icontains=valor) |
                Q(origem__icontains=valor) |
                Q(data_lancamento__icontains=valor) |
                Q(usuario__username__icontains=valor) |
                Q(id__icontains=valor)
            )
        else:
            object_list = self.model.objects.all()

        paginator = Paginator(object_list, 10)  # Show 10 contas per page

        page = self.request.GET.get('page')
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            queryset = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            queryset = paginator.page(paginator.num_pages)

        # return object_list
        return queryset


class MovimentoContabilHeaderCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = MovimentoContabilHeader
    form = MovimentoContabilHeaderForm()
    fields = ['tipo_movimento', 'data_competencia', 'usuario']
    context_object_name = 'movimentocontabilheader'
    template_name = "ctb/movimento_contabil_header/movimentocontabilheader_form.html"


class MovimentoContabilHeaderDetalhe(SuccessMessageMixin, LoginRequiredMixin, DetailView):
    model = MovimentoContabilHeader
    context_object_name = 'movimentocontabilheader'
    template_name = 'ctb/movimento_contabil_header/movimento_contabil_header_detail.html'


class MovimentoContabilHeaderUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = MovimentoContabilHeader
    context_object_name = 'movimentocontabilheader'
    fields = '__all__'
    success_message = '%(data_competencia)s alterado com sucesso!'
    template_name = 'ctb/movimento_contabil_header/movimentocontabilheader_form.html'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            calculated_field=self.object.data_competencia,
        )


def movimento_contabil_header_delete(request, id=None):
    obj = get_object_or_404(MovimentoContabilHeader, id=id)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Registro apagado com sucesso!')
        return redirect('ctb:movimento-list')

    context = {
        'object': obj
    }
    return render(request, 'ctb/confirm_delete.html', context)


"""
=========================================================================================
    LANCAMENTOS
=========================================================================================
"""


class RazaoContabilList(SuccessMessageMixin, LoginRequiredMixin, ListView):
    model = LancamentoContabil
    template_name = 'ctb/lancamento_contabil/razao_contabil.html'

    def get_queryset(self):
        valor = self.request.GET.get('q')
        if valor:
            object_list = self.model.objects.filter(
                Q(d_c__icontains=valor) |
                Q(valor__icontains=valor) |
                Q(historico__icontains=valor) |
                Q(conta__codigo_conta__icontains=valor)
            )
        else:
            object_list = self.model.objects.all()

        paginator = Paginator(object_list, 7)  # Show 7 contas per page

        page = self.request.GET.get('page')
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            queryset = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            queryset = paginator.page(paginator.num_pages)

        # return object_list
        return queryset


def totaliza_lancamentos(movimentocontabilheader_id):
    movimentocontabilheader = get_object_or_404(MovimentoContabilHeader, pk=movimentocontabilheader_id)
    header_lancamentos = movimentocontabilheader.lancamentocontabil_set.all()

    total_debito = header_lancamentos.filter(d_c='D').aggregate(Sum('valor'))
    total_credito = header_lancamentos.filter(d_c='C').aggregate(Sum('valor'))

    # total_debito = total_debito.values()

    # total_credito = total_credito.values()

    # movimentocontabilheader.total_debito = total_debito
    # movimentocontabilheader.total_credito = total_credito
    # movimentocontabilheader.save()


def saldo_anterior(codigo_conta):
    ultimo_id = LancamentoContabil.objects.filter(conta=codigo_conta).aggregate(Max('id'))
    if not ultimo_id:
        return 0
    else:
        lancamento = LancamentoContabil.objects.filter(pk=ultimo_id['id__max'])
        if not lancamento:
            return 0
        else:
            return lancamento.saldo_final


def pega_natureza_conta(conta_id):
    obj = get_object_or_404(Conta, pk=conta_id)
    return obj.natureza


def create_lancamento(request, movimentocontabilheader_id):
    form = LancamentoContabilForm(request.POST or None, request.FILES or None)
    movimentocontabilheader = get_object_or_404(MovimentoContabilHeader, pk=movimentocontabilheader_id)
    if form.is_valid():
        header_lancamentos = movimentocontabilheader.lancamentocontabil_set.all()
        for l in header_lancamentos:
            if l.conta == form.cleaned_data.get("conta"):
                context = {
                    'movimentocontabilheader': movimentocontabilheader,
                    'form': form,
                    'error_message': 'Você já utilizou esse código de Conta',
                }
                return render(request, 'ctb/lancamento_contabil/create_lancamentocontabil.html', context)

        lancamentocontabil = form.save(commit=False)
        lancamentocontabil.header = movimentocontabilheader

        lancamentocontabil.saldo_anterior = saldo_anterior(lancamentocontabil.conta)

        natureza = pega_natureza_conta(lancamentocontabil.conta_id)
        if natureza == 'D':
            """Aqui o Débito AUMENTA o saldo"""
            if lancamentocontabil.d_c == 'D':
                lancamentocontabil.saldo_final = lancamentocontabil.saldo_anterior + lancamentocontabil.valor
            else:
                lancamentocontabil.saldo_final = lancamentocontabil.saldo_anterior - lancamentocontabil.valor
            print("Conta: " + str(lancamentocontabil.conta) + " Natureza: " + str(
                natureza) + " DC: " + lancamentocontabil.d_c +
                  " Saldo Final: " + str(lancamentocontabil.saldo_final))
        else:
            """Aqui o Crédito AUMENTA o saldo"""
            if lancamentocontabil.d_c == 'C':
                lancamentocontabil.saldo_final = lancamentocontabil.saldo_anterior + lancamentocontabil.valor
            else:
                lancamentocontabil.saldo_final = lancamentocontabil.saldo_anterior - lancamentocontabil.valor

        lancamentocontabil.save()

        if lancamentocontabil.d_c == 'D':
            movimentocontabilheader.total_debito += lancamentocontabil.valor
        else:
            movimentocontabilheader.total_credito += lancamentocontabil.valor

        movimentocontabilheader.save()

        return render(request, 'ctb/movimento_contabil_header/movimento_contabil_header_detail.html',
                      {'movimentocontabilheader': movimentocontabilheader})
    context = {
        'movimentocontabilheader': movimentocontabilheader,
        'form': form,
    }
    return render(request, 'ctb/lancamento_contabil/create_lancamentocontabil.html', context)


# def detail_lancamento(request, movimentocontabilheader_id):
#         user = request.user
#         movimentocontabilheader = get_object_or_404(MovimentoContabilHeader, pk=movimentocontabilheader_id)
#         return render(request, 'ctb/lancamento_contabil/lancamento_contabil_detail.html',
#                       {'movimentocontabilheader': movimentocontabilheader, 'user': user})


def delete_lancamento(request, movimentocontabilheader_id, lancamentocontabil_id):
    movimentocontabilheader = get_object_or_404(MovimentoContabilHeader, pk=movimentocontabilheader_id)
    lancamento = LancamentoContabil.objects.get(pk=lancamentocontabil_id)

    if lancamento.d_c == 'D':
        movimentocontabilheader.total_debito -= lancamento.valor
    else:
        movimentocontabilheader.total_credito -= lancamento.valor

    movimentocontabilheader.save()

    lancamento.delete()

    totaliza_lancamentos(movimentocontabilheader_id)

    return render(request, 'ctb/movimento_contabil_header/movimento_contabil_header_detail.html',
                  {'movimentocontabilheader': movimentocontabilheader})


class LancamentoContabilDetalhe(SuccessMessageMixin, LoginRequiredMixin, DetailView):
    model = LancamentoContabil
    context_object_name = 'lancamento'
    template_name = 'ctb/lancamento_contabil/lancamento_contabil_detail.html'


class LancamentoContabilUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = LancamentoContabil
    fields = '__all__'
    success_message = '%(conta)s alterado com sucesso!'
    template_name = 'ctb/lancamento_contabil/lancamentocontabil_form.html'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            calculated_field=self.object.conta,
        )


def lancamento_contabil_delete(request, id=None):
    obj = get_object_or_404(LancamentoContabil, id=id)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Registro apagado com sucesso!')
        return redirect('ctb:lancamento-list')

    context = {
        'object': obj
    }
    return render(request, 'ctb/confirm_delete.html', context)


"""
=========================================================================================
    FIM DO BLOCO DE LANCAMENTOS
=========================================================================================
"""

"""
    SALDOS CONTÁBEIS
"""


class SaldoContaContabilList(ListView):
    model = SaldoContaContabil
    context_object_name = 'saldo'
    template_name = 'ctb/saldo/saldo-list.html'

    def get_queryset(self):
        valor = self.request.GET.get('q')
        if valor:
            object_list = self.model.objects.filter(
                Q(conta__codigo_conta__icontains=valor) |
                Q(conta__descricao__icontains=valor) |
                Q(conta__codigo_conta__startswith=valor) |
                Q(debitos__icontains=valor) |
                Q(creditos__icontains=valor) |
                Q(saldo_inicial__icontains=valor)
            )
        else:
            object_list = self.model.objects.all()

        paginator = Paginator(object_list, 12)  # Show 10 contas per page

        page = self.request.GET.get('page')
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            queryset = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            queryset = paginator.page(paginator.num_pages)

        # return object_list
        return queryset


class SaldoDetalhe(DetailView):
    model = SaldoContaContabil
    context_object_name = 'saldo'
    template_name = "ctb/saldo/saldo_detalhe.html"


class SaldoUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = SaldoContaContabil
    fields = '__all__'
    success_message = '%(data_competencia)s alterado com sucesso!'
    template_name = 'ctb/competencia/competencia_form.html'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            calculated_field=self.object.data_competencia,
        )


"""
     USO DO FORMSET
"""


class LancamentoContabilCreate(CreateView):
    model = MovimentoContabilHeader
    context_object_name = 'header'
    fields = ['tipo_movimento', 'usuario', 'data_competencia']
    success_message = '%(name) criado com sucesso!'
    success_url = reverse_lazy('ctb:movimento-list')
    template_name = "ctb/movimento_contabil_header/movimentocontabilheader_form.html"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            calculated_field=self.object.name,
        )

    def get_context_data(self, **kwargs):
        data = super(LancamentoContabilCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['lancamentos'] = LancamentoContabilFormSet(self.request.POST)
        else:
            data['lancamentos'] = LancamentoContabilFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        lancamentos = context['lancamentos']
        with transaction.atomic():
            self.object = form.save()

            if lancamentos.is_valid():
                lancamentos.instance = self.object
                lancamentos.save()
        return super(LancamentoContabilCreate, self).form_valid(form)


"""
     FIM USO DO FORMSET
"""

"""
  404 & 500
"""


def error_404(request):
    return render(request, '404.html', {})


def error_500(request):
    return render(request, '500.html', {})
