from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView, DetailView, UpdateView

from ctb.forms import ContaForm
from ctb.models import Conta, Historico, Empresa, Competencia, MovimentoContabilHeader, MovimentoContabil

"""
    PÁGINA PRINCIPAL DA CONTABILIDADE 
"""


@login_required(login_url='/admin/login')
def ctb_index(request):
    context = {
                'title': 'Menu Principal',
                'current_user': request.user,
    }

    return render(request, "index.html", context)

"""
       PLANO DE CONTAS
"""


class ContaList(SuccessMessageMixin, LoginRequiredMixin, ListView):
    model = Conta
    template_name = "ctb/conta/conta-list.html"

    def get_queryset(self):
        descricao = self.request.GET.get('q')
        if descricao:
            object_list = self.model.objects.filter(descricao__icontains=descricao)
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
    success_message = 'Detalhe registro apresentado com sucesso!'
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
    template_name = 'ctb/movimento_contabil_header/movimento_contabil_header-list.html'

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


class MovimentoContabilHeaderCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = MovimentoContabilHeader
    fields = '__all__'
    template_name = "ctb/movimento_contabil_header/movimentocontabilheader_form.html"


class MovimentoContabilHeaderDetalhe(SuccessMessageMixin, LoginRequiredMixin, DetailView):
    model = MovimentoContabilHeader
    context_object_name = 'movimento'
    template_name = 'ctb/movimento_contabil_header/movimento_contabil_header_detail.html'


class MovimentoContabilHeaderUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = MovimentoContabilHeader
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
    Movimentos Contabeis  - LANCAMENTOS
"""


class MovimentoContabilList(SuccessMessageMixin, LoginRequiredMixin, ListView):
    model = MovimentoContabil
    template_name = 'ctb/movimento_contabil/movimento_contabil-list.html'

    def get_queryset(self):
        conta = self.request.GET.get('q')
        if conta:
            object_list = self.model.objects.filter(conta__icontains=conta)
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


class MovimentoContabilCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = MovimentoContabil
    fields = '__all__'
    template_name = "ctb/movimento_contabil/movimentocontabil_form.html"


class MovimentoContabilDetalhe(SuccessMessageMixin, LoginRequiredMixin, DetailView):
    model = MovimentoContabil
    context_object_name = 'lancamento'
    template_name = 'ctb/movimento_contabil/movimento_contabil_detail.html'


class MovimentoContabilUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = MovimentoContabil
    fields = '__all__'
    success_message = '%(data_competencia)s alterado com sucesso!'
    template_name = 'ctb/movimento_contabil/movimentocontabil_form.html'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            calculated_field=self.object.conta,
        )


def movimento_contabil_delete(request, id=None):
    obj = get_object_or_404(MovimentoContabil, id=id)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Registro apagado com sucesso!')
        return redirect('ctb:lancamento-list')

    context = {
        'object': obj
    }
    return render(request, 'ctb/confirm_delete.html', context)
