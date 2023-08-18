from django.contrib import admin
from troca_turno.models import Operacao, MobyUser, Torre, Passagem

admin.site.register(Operacao)
admin.site.register(MobyUser)
admin.site.register(Torre)
admin.site.register(Passagem)
