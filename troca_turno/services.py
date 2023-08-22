from troca_turno.models import MobyUser, Passagem, Torre, Operacao, Anexo

from django.contrib.auth import authenticate, login
from django.db import IntegrityError


DATABASE = 'default'

class MobyUserService:

    @staticmethod
    def query_all():
        usuarios = MobyUser.objects.using(DATABASE).all()
        return usuarios
    
    @staticmethod
    def get(id):
        try:
            usuario = MobyUser.objects.using(DATABASE).get(id=id)
            return usuario
        
        except MobyUser.DoesNotExist:
            return None
     
    @staticmethod
    def get_email(email):
        try:
            usuario = MobyUser.objects.using(DATABASE).get(email=email)
            return usuario
        
        except MobyUser.DoesNotExist:
            return None
        
    @staticmethod
    def aut(request, email, senha):
        usuario = authenticate(request, email=email, password=senha)

        if usuario:
            login(request, usuario)

            return True
        
        else:
            return False
        
    @staticmethod
    def op_filter(request):
        usuarios = MobyUser.objects.using(DATABASE).filter(operacao=request.user.operacao).all()
        return usuarios
        

class PassagemService:

    @staticmethod
    def generic():
        return Passagem.objects.using(DATABASE)
    
    @staticmethod
    def query_all():
        passagens = Passagem.objects.using(DATABASE).all()
        return passagens
    
    @staticmethod
    def op_filter(request):
        operacao = request.user.operacao
        passagens = Passagem.objects.using(DATABASE).all().order_by('concluida').filter(torre__operacao=operacao)
        return passagens
    
    @staticmethod
    def create(titulo, descricao, torre, responsavel, receptor):
        try:
            passagem = Passagem.objects.using(DATABASE).create(
                titulo=titulo,
                descricao=descricao,
                torre=torre,
                responsavel=responsavel,
                receptor=receptor
            )

            return passagem
        
        except IntegrityError as e:
            return e
    

class TorreService:

    @staticmethod
    def query_all():
        torres = Torre.objects.using(DATABASE).all()
        return torres
    
    @staticmethod
    def create(numero, operacao):
        torre = Torre.objects.using(DATABASE).filter(numero=numero).filter(operacao=operacao).first()

        if torre:
            return False

        else:
            Torre.objects.using(DATABASE).create(numero=numero, operacao=operacao).save()
            return True
        
    @staticmethod
    def get(numero, operacao):
        try:
            torre = Torre.objects.using(DATABASE).filter(numero=numero).filter(operacao=operacao).first()
        except:
            torre = None

        return torre
        
    @staticmethod
    def query_for_user(request):
        torres = Torre.objects.using(DATABASE).filter(operacao=request.user.operacao).all()
        return torres
        

class OperacaoService:

    @staticmethod
    def query_all():
        operacoes = Operacao.objects.using(DATABASE).all()
        return operacoes
    
    @staticmethod
    def get(nome):
        operacao = Operacao.objects.using(DATABASE).get(nome=nome)
        return operacao
    

class AnexoService:

    @staticmethod
    def query_all():
        anexos = Anexo.objects.using(DATABASE).all()
        return anexos
    
    @staticmethod
    def create(passagem):
        anexo = Anexo.objects.using(DATABASE).create(passagem=passagem)

        if anexo:
            return anexo
        
        else:
            return None

