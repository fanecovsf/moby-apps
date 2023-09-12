from django.urls import path
from django.contrib.auth import views as auth_views

from troca_turno.views import Views

urlpatterns = [
    path("", Views.red_painel, name="red-painel"),
    path("register/", Views.registro_usuario, name='registro-usuario'),
    path('painel/', Views.painel_principal, name='painel-principal'),
    path('painel/cadastro-torre/', Views.cadastro_torre, name='cadastro-torre'),
    path('painel/registro-passagem', Views.registro_passagem, name='registro-passagem'),
    path('painel/<id>', Views.edit_passagem, name='edit-passagem'),
    path('painel/view/<id>', Views.view_passagem, name='view-passagem'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]


