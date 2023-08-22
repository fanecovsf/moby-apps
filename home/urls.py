from django.urls import path

from home.views import Views

urlpatterns = [
    path('', Views.home_page, name='home-page')
]