from django.contrib import admin

# Register your models here.
from ctb.models import Conta, Historico, Competencia

admin.site.register(Competencia)
admin.site.register(Conta)
admin.site.register(Historico)
