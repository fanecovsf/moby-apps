from djongo import models

class DT(models.Model):

    documento = models.CharField(max_length=255, primary_key=True)
    descricao = models.CharField(max_length=1000)

    objects = models.DjongoManager()

    class Meta:
        managed = False
        db_table = "tb_viagens"
        abstract = False