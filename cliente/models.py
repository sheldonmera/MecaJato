from django.db import models

# Create your models here.
class Cliente(models.Model):
    nome = models.CharField(max_length=200)
    sobrenome = models.CharField(max_length=200)
    email = models.EmailField(max_length=50)
    cpf = models.CharField(max_length=11)
    
    def __str__(self):
        return self.nome
    

class Carro(models.Model):
    modelo = models.CharField(max_length=200)
    placa = models.CharField(max_length=7)
    ano = models.IntegerField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    cont_lavagem = models.IntegerField(default=0)
    cont_conserto = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return self.modelo