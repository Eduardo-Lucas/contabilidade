from django.contrib import admin
from glb.models import GlobalEmpresa, GlobalCodigoCnae, GlobalMunicipio, GlobalNaturezaJuridica, GlobalCodigoEstado

# Register your models here.

admin.site.register(GlobalCodigoCnae)
admin.site.register(GlobalCodigoEstado)
admin.site.register(GlobalEmpresa)
admin.site.register(GlobalMunicipio)
admin.site.register(GlobalNaturezaJuridica)
