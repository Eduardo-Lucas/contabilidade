from django import forms

from .models import Conta


class ContaForm(forms.ModelForm):
    class Meta:
        model = Conta
        fields = [
                  'codigo_conta', 'descricao', 'tipo_conta', 'conta_ativa', 'grau_conta', 'conta_superior',
                  'conta_saldo_balanco', 'origem', 'natureza', 'conta_referencial_bacen', 'conta_referencial_dinamica',
                  'conta_referencial_susep'
                 ]
