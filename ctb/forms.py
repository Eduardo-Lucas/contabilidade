from django.forms import ModelForm

from ctb.models import Conta, LancamentoContabil, MovimentoContabilHeader


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


class MovimentoContabilHeaderForm(ModelForm):
    class Meta:
        model = MovimentoContabilHeader
        fields = '__all__'


class LancamentoContabilForm(ModelForm):
    class Meta:
        model = LancamentoContabil
        fields = ['conta', 'valor', 'd_c', 'codigo_historico', 'historico', 'codigo_participante', 'tipo_documento', \
                  'numero_documento', 'data_documento']
