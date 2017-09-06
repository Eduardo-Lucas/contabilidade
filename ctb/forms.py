from django.forms import ModelForm

from ctb.models import Conta


# Forms
class ContaForm(ModelForm):
        class Meta:
            model = Conta
            fields = '__all__'
            """
            fields = [
                  'codigo_conta', 'descricao', 'conta_saldo_balanco', 'origem', 'natureza', 'conta_referencial_bacen',
                  'conta_referencial_dinamica', 'conta_referencial_susep'
                 ]
            
            exclude = [
                'tipo_conta', 'conta_superior', 'conta_ativa', 'grau_conta'
            ]
            """