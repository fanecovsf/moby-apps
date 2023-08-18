from django.db import models
from django.contrib.auth.models import AbstractUser, User


class Operacao(models.Model):
    nome = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.nome


class MobyUser(AbstractUser):
    #username & password charfield

    operacao = models.ForeignKey(Operacao, related_name='operacoesUser', on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self) -> str:
        return self.username


class Torre(models.Model):
    numero = models.IntegerField()
    data_cadastro = models.DateTimeField(auto_now_add=True)
    operacao = models.ForeignKey(Operacao, related_name='operacoesTorre', on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f'Torre {self.numero}'


class Passagem(models.Model):
    titulo = models.CharField(max_length=60)
    descricao = models.CharField(max_length=5000)

    torre = models.OneToOneField(
        Torre,
        on_delete=models.DO_NOTHING
    )

    responsavel = models.OneToOneField(
        MobyUser,
        related_name='passagem_responsavel',
        on_delete=models.DO_NOTHING
    )

    receptor = models.OneToOneField(
        MobyUser,
        related_name='passagem_receptor',
        on_delete=models.DO_NOTHING
    )

    anexo = models.FileField(upload_to='attachments/', null=True, blank=True)
    concluida = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.titulo

