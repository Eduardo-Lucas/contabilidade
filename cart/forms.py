from django import forms

from choices.models import DEBITO_CREDITO_CHOICES
from ctb.models import Historico, Conta


class CartAddLancamentoForm(forms.Form):
    conta = forms.ModelChoiceField(queryset=Conta.objects.filter(conta_ativa=True, tipo_conta='A'))
    valor = forms.DecimalField(max_digits=16, decimal_places=2, localize=True)
    d_c = forms.TypedChoiceField(label='D_C', choices=DEBITO_CREDITO_CHOICES)
    codigo_historico = forms.ModelChoiceField(label='Código Histórico', queryset=Historico.objects.all())
    historico = forms.CharField(label='Histórico', max_length=250)
