from django.db import models
from datetime import datetime
from pessoas.models import Pessoa


class Receita(models.Model):
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    nome_receita = models.CharField(max_length=255)
    ingredientes = models.TextField()
    modo_preparo = models.TextField()
    tempo_preparo = models.IntegerField()
    rendimento = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    data_receita = models.DateField(default=datetime.now, blank=True)
    imagem_receita = models.ImageField(upload_to='imagem/%d/%m/%Y/', blank=True)
    publicada = models.BooleanField(default=False)



