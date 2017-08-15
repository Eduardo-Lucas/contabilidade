from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from ctb.models import Historico, Conta, Empresa

from .forms import ContaForm

"""
    PÁGINA PRINCIPAL DA CONTABILIDADE 
"""


def ctb_index(request):
    context = {
                'title': 'Menu Principal',
                'current_user': request.user,
                'empresas': {},
    }

    return render(request, "index.html", context)

"""
       PLANO DE CONTAS
"""


@login_required(login_url="acc/login")
def conta_create(request):
    # empresa = UserProfile.objects.filter(usuario=request.user.id)
    print(request.user.id)
    form = ContaForm(request.POST or None, initial={'empresa': 1})
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
    context = {
        "title": "Cria Nova Conta Contábil",
        "form": form
    }
    return render(request, "ctb/conta_form.html", context)


@login_required(login_url="acc/login")
def conta_detail(request, conta_id):
    # instance = Conta.objects.get(id=1)
    conta = get_object_or_404(Conta, pk=conta_id)
    context = {
        "conta": conta
    }
    return render(request, "ctb/conta_detail.html", context)


@login_required(login_url="acc/login")
def conta_list(request):
    all_contas = Conta.objects.all()
    context = {
        "all_contas": all_contas
    }
    return render(request, "ctb/conta.html", context)


@login_required(login_url="acc/login")
def conta_update(request):
    return HttpResponse("<h1>Update</h1>")


@login_required(login_url="acc/login")
def conta_delete(request):
    return HttpResponse("<h1>Delete</h1>")


"""
    WORK IN PROGRESS
"""


def work_in_progress(request):
    return render(request, "wip.html", {})
