from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from ctb.models import Conta
from .cart import Cart
from .forms import CartAddLancamentoForm


@require_POST
def cart_add(request, conta_id):
    cart = Cart(request)
    conta = get_object_or_404(Conta, id=conta_id)
    form = CartAddLancamentoForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(conta=conta,
                 valor=cd['valor'],
                 d_c=cd['d_c'],
                 codigo_historico=cd['codigo_historico'],
                 historico=cd['historico'])
    return redirect('cart:cart_detail')


def cart_remove(request, conta_id):
    cart = Cart(request)
    conta = get_object_or_404(Conta, id=conta_id)
    cart.remove(conta)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})
