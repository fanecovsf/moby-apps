from django.urls import path

from troca_turno.views import Views

urlpatterns = [
    path('login/', Views.login_app, name='login'),
    path('painel/', Views.painel_principal, name='painel-principal'),
    path('painel/cadastro-torre/', Views.cadastro_torre, name='cadastro-torre')
]