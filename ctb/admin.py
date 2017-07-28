from django.contrib import admin

# Register your models here.
from ctb.models import Conta, Historico

admin.site.register(Historico)
admin.site.register(Conta)
