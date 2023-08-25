from django.shortcuts import render, redirect
from django.http.response import HttpResponse

from troca_turno.mongo_models import DT

def test_view(request):
    dts = DT.objects.using('mongo-default').all()

    return render(request, 'mongo-view.html', context={
        'dts': dts
    })