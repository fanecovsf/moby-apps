from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from troca_turno.services import MobyUserService, PassagemService, TorreService, OperacaoService, ViagensService
from troca_turno.forms import MobyUserCreationForm

import datetime

class Views:


    @login_required(login_url='/login/')
    def red_painel(request):
        return redirect('painel-principal')


    @login_required(login_url='/login/')
    def painel_principal(request):
        user = request.user
        passagens = PassagemService.op_filter(request)
        torres = TorreService.query_for_user(request)
        usuarios = MobyUserService.op_filter(request)

        is_manager = MobyUserService.is_manager(user)

        data_final = timezone.make_aware(timezone.datetime.now().replace(hour=23, minute=59, second=59))
        data_inicial = data_final - timezone.timedelta(days=2)
        
        data_final = data_final.strftime("%Y-%m-%d %H:%M:%S")
        data_inicial = data_inicial.strftime("%Y-%m-%d %H:%M:%S")

        if request.method == 'POST':
            data_inicio = request.POST.get('data-inicio')
            data_fim = request.POST.get('data-fim')
            filtro_torre = TorreService.get(request.POST.get('filtro-torre'), request.user.operacao)
            filtro_resp = MobyUserService.get_email(request.POST.get('filtro-resp'))
            filtro_recep = MobyUserService.get_email(request.POST.get('filtro-recep'))
            filtro_title = request.POST.get('filtro-title')

            filtro_status = request.POST.get('filtro-status')
            if filtro_status == 'concluido':
                filtro_status = True

            elif filtro_status == 'pendente':
                filtro_status = False

            else:
                pass

            if data_inicio and data_fim:
                data_inicio = data_inicio + " 00:00:00"
                data_inicio = timezone.datetime.strptime(data_inicio, "%Y-%m-%d %H:%M:%S")

                data_fim = data_fim + " 23:59:59"
                data_fim = timezone.datetime.strptime(data_fim, "%Y-%m-%d %H:%M:%S")

                passagens = passagens.filter(criado_em__range=(data_inicio,data_fim))

            if filtro_torre:
                passagens = passagens.filter(torre=filtro_torre)

            if filtro_title:
                passagens = passagens.filter(titulo__contains=filtro_title)

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
                'usuarios': usuarios,
                'is_manager': is_manager,
            })

        if request.method == 'GET':
            passagens = passagens.filter(criado_em__range=(data_inicial, data_final))

            return render(request, 'painel.html', context={
                'user':user,
                'passagens':passagens,
                'torres': torres,
                'usuarios': usuarios,
                'is_manager': is_manager,
            })
        
    
    @login_required(login_url='/login/')
    def mudar_senha(request):
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Sua senha foi alterada com sucesso!")
                return redirect('mudar-senha')
            else:
                messages.error(request, "Erro ao mudar sua senha, verifique a senha digitada.")
        else:
            form = PasswordChangeForm(request.user)
        return render(request, 'mudar-senha.html', context={
            'form':form
        })
        
    
    @login_required(login_url='/login/')
    def registro_usuario(request):
        created = 0
        if request.method == "POST":
            form = MobyUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Usuário registrado com sucesso.")
                created = 1
                return render(request, 'registro-usuario.html', context={
                    'form': form,
                    'created': created
                })
            else:
                created = 2
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"Erro no campo {field}: {error}")

                return render(request, 'registro-usuario.html', context={
                    'form': form,
                    'created': created
                })
                
        form = MobyUserCreationForm()
        return render(request=request, template_name="registro-usuario.html", context={"form":form})
    

    @login_required(login_url='/login/')
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
    

    @login_required(login_url='/login/')
    def registro_passagem(request):
        user = request.user

        torres = TorreService.query_for_user(request)
        usuarios = MobyUserService.exclude_email(user.email)

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

                return redirect('painel-principal')

            except Exception as e:
                return HttpResponse({'error':'Erro ao criar a passagem', 'descricao':e})

        return render(request, 'registro-passagem.html', context={
            'torres':torres,
            'usuarios':usuarios
        })
    

    @login_required(login_url='/login/')
    def edit_passagem(request, id):
        popup_exists = False
        popup_added = False
        popup_dt_exists = False
        popup_blank = False
        popup_delete = False
        passagem = PassagemService.get(id)
        usuarios = MobyUserService.op_filter(request).exclude(email=request.user.email)
        dts = PassagemService.query_dts(passagem)

        dt_list = []

        if dts:
            for value in dts.values():
                dt = ViagensService.filter_dt(value)
                dt_list.append(dt)

        if request.method == 'POST':

            acao = request.POST.get('acao')

            if acao == 'salvar':
                titulo = request.POST.get('titulo')
                descricao = request.POST.get('descricao')
                receptor = MobyUserService.get_email(request.POST.get('receptor'))

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
            
            if acao == 'add-dt':
                dt = request.POST.get('DT')

                if dt != '':
                    try:
                        dt = ViagensService.filter_dt(dt)

                        if passagem.dt_lista:
                            num_dts = len(passagem.dt_lista)
                        else:
                            num_dts = 0

                        data = {
                            f'dt{num_dts+1}':dt['idPlanoViagem']
                        }

                        dt_lista = passagem.dt_lista or {}

                        value_exists = any(dt['idPlanoViagem'] == item for item in dt_lista.values())  
                        
                        if value_exists:
                            popup_exists = True

                        else:
                            popup_added = True
                            PassagemService.add_dt(passagem=passagem, data=data)

                    except:
                        popup_dt_exists = True

                else:
                    popup_blank = True

            if acao == 'delete-dt':
                dt = request.POST.get('dt-delete')
                PassagemService.remove_dt(passagem, dt)
                popup_delete = True
                

        dts = PassagemService.query_dts(passagem)

        dt_list = []

        if dts:
            for value in dts.values():
                dt = ViagensService.filter_dt(value)
                dt_list.append(dt)


        return render(request, 'edit-passagem.html', context={
            'passagem':passagem,
            'usuarios':usuarios,
            'popup_exists':popup_exists,
            'popup_added':popup_added,
            'popup_dt_exists':popup_dt_exists,
            'popup_blank':popup_blank,
            'dt_list':dt_list,
            'popup_delete':popup_delete,
        })
    
    
    @login_required(login_url='/login/')
    def view_passagem(request, id):
        passagem = PassagemService.get(id)

        dts = PassagemService.query_dts(passagem)

        dt_list = []

        if dts:
            for value in dts.values():
                dt = ViagensService.filter_dt(value)
                dt_list.append(dt)

        return render(request, 'view-passagem.html', context={
            'passagem': passagem,
            'dt_list': dt_list,
        })




