from djongo import models

class AlertasOperador(models.Model):

    _id = models.CharField(max_length=500, primary_key=True)
    OPERADOR = models.CharField(max_length=255)
    ALERTA = models.CharField(max_length=255)

    objects = models.DjongoManager()

    class Meta:
        managed = False
        db_table = "AlertasOperador"
        abstract = False