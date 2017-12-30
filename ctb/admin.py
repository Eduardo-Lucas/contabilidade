from django.contrib import admin

# Register your models here.
from ctb.models import Conta, Historico, Competencia, MovimentoContabilHeader, LancamentoContabil, SaldoContaContabil, \
    TipoMovimento, TipoDocumento

admin.site.register(Competencia)
admin.site.register(Conta)
admin.site.register(Historico)
admin.site.register(LancamentoContabil)
admin.site.register(MovimentoContabilHeader)
admin.site.register(SaldoContaContabil)
admin.site.register(TipoDocumento)
admin.site.register(TipoMovimento)
