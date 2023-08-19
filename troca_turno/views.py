from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required

from troca_turno.services import MobyUserService, PassagemService

class Views:

    @staticmethod
    def login_app(request):
        if request.method == 'POST':
            email = request.POST.get('email')
            senha = request.POST.get('senha')
            
            login = MobyUserService.aut(request, email, senha)

            if login:
                return redirect('painel-principal')
            
            else:
                render(request, 'login.html')

        return render(request, 'login.html')


    @login_required(login_url='/troca-turno/login/')
    def painel_principal(request):
        user = request.user
        passagens = None

        return render(request, 'painel.html', context={
            'user':user,
            'passagens':passagens
        })