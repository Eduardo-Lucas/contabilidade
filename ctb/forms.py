# coding=utf-8
from decimal import Decimal

from django.forms import ModelForm, inlineformset_factory, BaseInlineFormSet

from ctb.models import Conta, MovimentoContabilHeader, LancamentoContabil


class ContaForm(ModelForm):
    class Meta:
        model = Conta
        fields = ['codigo_conta', 'descricao', 'tipo_conta', 'conta_ativa', 'grau_conta', 'conta_superior',
                  'conta_saldo_balanco', 'origem', 'natureza', 'conta_referencial_bacen', 'conta_referencial_dinamica',
                  'conta_referencial_susep']
        exclude = ['conta_ativa', 'data_inclusao']


class MovimentoContabilHeaderForm(ModelForm):
    class Meta:
        model = MovimentoContabilHeader
        fields = ['tipo_movimento', 'data_competencia']
        exclude = ['usuario', 'total_debito', 'total_credito']


class LancamentoContabilForm(ModelForm):
    class Meta:
        model = LancamentoContabil
        fields = ['conta', 'valor', 'd_c', 'codigo_historico', 'historico']
        exclude = ['saldo_anterior', 'saldo_final', 'codigo_participante', 'tipo_documento',
                   'numero_documento', 'data_documento']


class CustomLancamentoInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        tot_deb, tot_cred = Decimal(0.00), Decimal(0.00)
        for form in self.forms:
            dc = form.cleaned_data.get('d_c')
            if dc is not None:
                valor = form.cleaned_data.get('valor')
                if dc == 'D':
                    tot_deb += valor
                else:
                    tot_cred += valor

        if tot_deb != tot_cred:
            self.add_error('valor', 'A soma de Débitos e Créditos está DIFERENTE!')

        return self.cleaned_data


LancamentoContabilFormSet = inlineformset_factory(MovimentoContabilHeader, LancamentoContabil,
                                                  form=LancamentoContabilForm,
                                                  fields=('conta', 'valor', 'd_c', 'codigo_historico', 'historico'),
                                                  extra=8,
                                                  can_delete=False,
                                                  min_num=2,
                                                  validate_min=True,
                                                  formset=CustomLancamentoInlineFormSet)
