from django.urls import path

from troca_turno.views import Views

urlpatterns = [
    path('login/', Views.login_app, name='login')
]