from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('troca-turno/', include('troca_turno.urls')),
    path('', include('home.urls'))
]
