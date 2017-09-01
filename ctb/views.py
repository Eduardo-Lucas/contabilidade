from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.http import request, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from ctb.models import Conta, Historico


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
    fields = '__all__'
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

