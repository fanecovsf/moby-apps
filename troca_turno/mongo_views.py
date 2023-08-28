from django.shortcuts import render, redirect
from django.http.response import HttpResponse

from troca_turno.mongo_models import AlertasOperador

def test_view(request):
    dts = AlertasOperador.objects.using('mongo-default').first()

    return render(request, 'mongo-view.html', context={
        'dts': dts
    })