from django.shortcuts import render, redirect

from troca_turno.services import MobyUserService

class Views:

    @staticmethod
    def home_page(request):
        return redirect('login')
    
    @staticmethod
    def login_app(request):
        login_fail = False

        user = request.user

        if user.is_authenticated:
            return redirect('painel-principal')

        if request.method == 'POST':
            email = request.POST.get('email')
            senha = request.POST.get('senha')
            
            login = MobyUserService.aut(request, email, senha)

            if login:
                return redirect('painel-principal')
            
            else:
                login_fail = True
                return render(request, 'login.html', context={
                    'login_fail': login_fail,
                })

        return render(request, 'login.html', context={
            'login_fail': login_fail
        })
