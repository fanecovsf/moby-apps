from django.urls import path
from django.contrib.auth import views as auth_views

from troca_turno.views import Views
from troca_turno.mongo_views import test_view

urlpatterns = [
    path('login/', Views.login_app, name='login'),
    path('painel/', Views.painel_principal, name='painel-principal'),
    path('painel/cadastro-torre/', Views.cadastro_torre, name='cadastro-torre'),
    path('painel/registro-passagem', Views.registro_passagem, name='registro-passagem'),
    path('painel/<id>', Views.edit_passagem, name='edit-passagem'),
    path('painel/view/<id>', Views.view_passagem, name='view-passagem'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path('mongo/', test_view, name='mongo-test')
]