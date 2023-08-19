from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required

from troca_turno.services import MobyUserService, PassagemService, TorreService, OperacaoService

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
                return render(request, 'login.html')

        return render(request, 'login.html')


    @login_required(login_url='/troca-turno/login/')
    def painel_principal(request):
        user = request.user
        passagens = PassagemService.op_filter(user.operacao)

        return render(request, 'painel.html', context={
            'user':user,
            'passagens':passagens
        })
    

    @login_required(login_url='/troca-turno/login/')
    def cadastro_torre(request):
        operacoes = OperacaoService.query_all()

        if request.method == 'POST':
            numero = request.POST.get('numero')
            operacao = OperacaoService.get(request.POST.get('operacao'))

            torre_create = TorreService.create(numero, operacao)

            if torre_create:
                return redirect('painel-principal')

            else:
                return HttpResponse('Torre já existente, tente novamente!')
            
        return render(request, 'cadastro-torre.html', context={
            'operacoes': operacoes
        })

