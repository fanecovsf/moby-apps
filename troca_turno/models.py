from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser, BaseUserManager

from troca_turno.util.util import Utils


#Tables já existentes
class Viagens(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    idPlanoViagem = models.CharField(max_length=50)
    idVeiculo = models.CharField(max_length=100)
    idCarreta = models.CharField(max_length=7)
    transportador = models.CharField(max_length=1000)


    def __str__(self):
        return self.idPlanoViagem
    
    class Meta:
        db_table = '"public"."Viagens"'
        managed = False



#Tables novas
class Operacao(models.Model):
    nome = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.nome

class MobyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O email deve ser definido")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class MobyUser(AbstractUser):
    #username & password charfield

    email = models.EmailField(("email_address"), unique=True)
    operacao = models.ForeignKey(Operacao, related_name='operacoesUser', on_delete=models.PROTECT, blank=True, null=True)
    nome_atlas = models.CharField(max_length=255, unique=True, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = MobyUserManager()

    def __str__(self) -> str:
        return self.email


class Torre(models.Model):
    numero = models.IntegerField()
    data_cadastro = models.DateTimeField(auto_now_add=True)
    operacao = models.ForeignKey(Operacao, related_name='operacoesTorre', on_delete=models.PROTECT)

    def __str__(self) -> str:
        return str(self.numero)


class Passagem(models.Model):
    titulo = models.CharField(max_length=60)
    descricao = models.CharField(max_length=5000)
    criado_em = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    finalizado_em = models.DateTimeField(null=True, blank=True)

    torre = models.ForeignKey(
        Torre,
        related_name='passagem_torre',
        on_delete=models.DO_NOTHING
    )

    responsavel = models.ForeignKey(
        MobyUser,
        related_name='passagem_responsavel',
        on_delete=models.DO_NOTHING
    )

    receptor = models.ForeignKey(
        MobyUser,
        related_name='passagem_receptor',
        on_delete=models.DO_NOTHING
    )

    dt_lista = models.JSONField(max_length=255, blank=True, null=True)

    concluida = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.titulo
    


