from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.files import File

from troca_turno.services import MobyUserService, PassagemService, TorreService, OperacaoService, AnexoService

import datetime

class Views:

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


    @login_required(login_url='/troca-turno/login/')
    def painel_principal(request):
        user = request.user
        passagens = PassagemService.op_filter(request)
        torres = TorreService.query_for_user(request)
        usuarios = MobyUserService.op_filter(request)

        data_final = datetime.date.today()
        data_inicial = data_final - datetime.timedelta(days=2)

        filtro_inicial = str(data_inicial) + " 00:00:00"
        filtro_final = str(data_final) + " 23:59:59"

        if request.method == 'POST':
            data_inicio = request.POST.get('data-inicio')
            data_fim = request.POST.get('data-fim')
            filtro_torre = TorreService.get(request.POST.get('filtro-torre'), request.user.operacao)
            filtro_resp = MobyUserService.get_email(request.POST.get('filtro-resp'))
            filtro_recep = MobyUserService.get_email(request.POST.get('filtro-recep'))

            filtro_status = request.POST.get('filtro-status')
            if filtro_status == 'concluido':
                filtro_status = True

            elif filtro_status == 'pendente':
                filtro_status = False

            else:
                pass

            if data_inicio and data_fim:
                data_inicio = data_inicio + " 00:00:00"
                data_fim = data_fim + " 23:59:59"
                passagens = passagens.filter(criado_em__range=(data_inicio,data_fim))

            if filtro_torre:
                passagens = passagens.filter(torre=filtro_torre)

            if filtro_resp:
                passagens = passagens.filter(responsavel=filtro_resp)

            if filtro_recep:
                passagens = passagens.filter(receptor=filtro_recep)

            if filtro_status==True or filtro_status==False:
                passagens = passagens.filter(concluida=filtro_status)

            return render(request, 'painel.html', context={
                'user':user,
                'passagens':passagens,
                'torres': torres,
                'usuarios': usuarios
            })

        if request.method == 'GET':
            passagens = passagens.filter(criado_em__range=(filtro_inicial, filtro_final))

            return render(request, 'painel.html', context={
                'user':user,
                'passagens':passagens,
                'torres': torres,
                'usuarios': usuarios,
                'data_inicial': str(data_inicial),
                'data_final': str(data_final)
            })
    

    @login_required(login_url='/troca-turno/login/')
    def cadastro_torre(request):
        operacao = request.user.operacao

        if request.method == 'POST':
            numero = request.POST.get('numero')

            torre_create = TorreService.create(numero, operacao)

            if torre_create:
                return redirect('painel-principal')

            else:
                return HttpResponse('Torre já existente, tente novamente!')
            
        return render(request, 'cadastro-torre.html', context={
            'operacao': operacao
        })
    

    @login_required(login_url='/troca-turno/login/')
    def registro_passagem(request):
        user = request.user

        torres = TorreService.query_for_user(request)
        usuarios = MobyUserService.query_all()

        if request.method == 'POST':
            try:
                titulo = request.POST.get('titulo')
                descricao = request.POST.get('descricao')
                torre = TorreService.get(request.POST.get('torre'), user.operacao)
                receptor = MobyUserService.get_email(request.POST.get('receptor'))
                passagem = PassagemService.create(
                    titulo=titulo,
                    descricao=descricao,
                    torre=torre,
                    responsavel=user,
                    receptor=receptor
                )

                if passagem:
                    anexos = request.FILES.getlist('anexos')

                    if anexos:
                        for anexo in anexos:
                            anexo_save = AnexoService.create(passagem=passagem)
                            anexo_save.arquivo.save(anexo.name, File(anexo))

                    return redirect('painel-principal')

                else:
                    return HttpResponse({'error':'Erro ao criar a passagem'})

            except Exception as e:
                return HttpResponse(e)

        return render(request, 'registro-passagem.html', context={
            'torres':torres,
            'usuarios':usuarios
        })
    

    @login_required(login_url='/troca-turno/login/')
    def edit_passagem(request, id):
        passagem = PassagemService.get(id)
        usuarios = MobyUserService.op_filter(request)

        if request.method == 'POST':

            acao = request.POST.get('acao')

            if acao == 'salvar':
                titulo = request.POST.get('titulo')
                descricao = request.POST.get('descricao')
                receptor = MobyUserService.get_email(request.POST.get('receptor'))

                anexos = request.FILES.getlist('anexos')
                if anexos:
                    for anexo in anexos:
                        anexo_save = AnexoService.create(passagem=passagem)
                        anexo_save.arquivo.save(anexo.name, File(anexo))

                passagem.titulo = titulo
                passagem.descricao = descricao
                passagem.receptor = receptor
                passagem.save()

                return redirect('painel-principal')
            
            if acao == 'finalizar':
                now = datetime.datetime.now()
                passagem.concluida = True
                passagem.finalizado_em = now

                passagem.save()

                return redirect('painel-principal')

        return render(request, 'edit-passagem.html', context={
            'passagem':passagem,
            'usuarios':usuarios
        })
    
    
    @login_required(login_url='/troca-turno/login/')
    def view_passagem(request, id):
        passagem = PassagemService.get(id)

        return render(request, 'view-passagem.html', context={
            'passagem':passagem
        })




