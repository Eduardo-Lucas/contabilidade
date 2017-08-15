from django.contrib import admin

from ctb.models import Empresa
from glb.models import GlobalCodigoCnae, GlobalMunicipio, GlobalNaturezaJuridica, GlobalCodigoEstado

# Register your models here.

admin.site.register(Empresa)
admin.site.register(GlobalCodigoCnae)
admin.site.register(GlobalCodigoEstado)
admin.site.register(GlobalMunicipio)
admin.site.register(GlobalNaturezaJuridica)
