from troca_turno.models import MobyUser, Passagem

from django.contrib.auth import authenticate, login


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
        

class PassagemService:
    
    @staticmethod
    def query_all():
        passagens = Passagem.objects.using(DATABASE).all()
        return passagens
    
    @staticmethod
    def op_filter(operacao):
        passagens = Passagem.objects.using(DATABASE).all().filter(operacao=operacao)
        return passagens
        

