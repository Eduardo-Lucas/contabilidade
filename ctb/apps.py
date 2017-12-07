from ctb.signals import aumenta_saldo, diminui_saldo, cria_saldo_contabil
from django.apps import AppConfig
from django.db.models.signals import post_save, pre_delete

from ctb.models import LancamentoContabil, Conta


class CtbConfig(AppConfig):
    name = 'ctb'

    def ready(self):
        post_save.connect(aumenta_saldo, sender=LancamentoContabil)
        pre_delete.connect(diminui_saldo, sender=LancamentoContabil)
        post_save.connect(cria_saldo_contabil, sender=Conta)
