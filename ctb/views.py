from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from ctb.models import Historico, Conta

from .forms import ContaForm
"""
       PLANO DE CONTAS
"""


def conta_create(request):
    form = ContaForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        print(form.cleaned_data.get("empresa"))
        instance.save()
    context = {
        "title": "Cria Nova Conta Contábil",
        "form": form
    }
    return render(request, "ctb/conta_form.html", context)


def conta_detail(request, conta_id):
    # instance = Conta.objects.get(id=1)
    conta = get_object_or_404(Conta, pk=conta_id)
    context = {
        "conta": conta
    }
    return render(request, "ctb/conta_detail.html", context)


def conta_list(request, empresa=1):
    all_contas = Conta.objects.filter(empresa=empresa)
    context = {
        "all_contas": all_contas
    }
    return render(request, "ctb/conta.html", context)


def conta_update(request):
    return HttpResponse("<h1>Update</h1>")


def conta_delete(request):
    return HttpResponse("<h1>Delete</h1>")
