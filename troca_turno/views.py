from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required

from troca_turno.services import MobyUserService

class Views:

    @staticmethod
    def login_app(request):
        if request.method == 'POST':
            email = request.POST.get('email')
            senha = request.POST.get('senha')
            
            login = MobyUserService.aut(request, email, senha)

            if login:
                return HttpResponse('Logado')
            
            else:
                return HttpResponse('Usuário não existente')

        return render(request, 'login.html')


    @login_required(login_url='/troca-turno/login/')
    def painel_principal(request):
        user = request.user
        passagens = None

        return render(request, 'painel.html', context={
            'user':user,
            'passagens':passagens
        })