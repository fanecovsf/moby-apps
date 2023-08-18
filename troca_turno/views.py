from django.shortcuts import render
from django.http.response import HttpResponse

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
