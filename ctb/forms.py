from django.forms import ModelForm, inlineformset_factory

from ctb.models import Conta, MovimentoContabilHeader, LancamentoContabil


class ContaForm(ModelForm):
    class Meta:
        model = Conta
        exclude = ['conta_ativa', 'data_inclusao']


class MovimentoContabilHeaderForm(ModelForm):
    class Meta:
        model = MovimentoContabilHeader
        exclude = ()


class LancamentoContabilForm(ModelForm):
    class Meta:
        model = LancamentoContabil
        exclude = ['saldo_anterior', 'saldo_final']


LancamentoContabilFormSet = inlineformset_factory(MovimentoContabilHeader, LancamentoContabil,
                                                  form=LancamentoContabilForm, extra=3, can_delete=True)
