from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.http import  request
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from ctb.models import Conta, Historico


"""
    PÁGINA PRINCIPAL DA CONTABILIDADE 
"""


@login_required(login_url='/acc/login')
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
    template_name = "ctb/conta.html"

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
    template_name = "ctb/conta_detail.html"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            calculated_field=self.object.descricao,
        )


class ContaCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Conta
    fields = '__all__'
    success_message = '%(descricao)s criado com sucesso!'
    template_name = "ctb/conta_form.html"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            calculated_field=self.object.descricao,
        )


class ContaUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Conta
    fields = '__all__'
    success_message = '%(descricao)s alterado com sucesso!'
    template_name = "ctb/conta_form.html"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            calculated_field=self.object.descricao,
        )


class ContaDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Conta
    template_name = "ctb/confirm_delete.html"
    success_url = reverse_lazy('ctb:conta-list')

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
    template_name = 'ctb/historico-index.html'


class HistoricoDetalhe(SuccessMessageMixin, LoginRequiredMixin, DetailView):
    model = Historico
    template_name = 'ctb/historico-detail.html'


class HistoricoCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Historico
    fields = '__all__'
    success_message = 'Registro criado com sucesso!'
    template_name = 'ctb/historico_form.html'

    def get_success_message(self, cleaned_data):
        return self.success_message


class HistoricoUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Historico
    fields = '__all__'
    success_message = '%(descricao)s alterado com sucesso!'
    template_name = 'ctb/historico_form.html'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            calculated_field=self.object.descricao,
        )


class HistoricoDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Historico
    template_name = 'ctb/confirm_delete.html'
    success_url = reverse_lazy('ctb:historico-list')
