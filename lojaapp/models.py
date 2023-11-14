from django.db import models
from django.contrib.auth.models import User


class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=200)
    endereco = models.CharField(max_length=200, null=True, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome_completo


class Categoria(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)


    def __str__(self):
        return self.titulo

class Produto(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.CharField(max_length=400)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to="produtos/")
    preco = models.PositiveIntegerField()
    venda = models.PositiveIntegerField()
    descricao = models.TextField()
    garantia = models.TextField(max_length=300, null=True, blank=True)
    devolucao = models.CharField(max_length=300, null=True, blank=True)
    visualizacao = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.titulo

class Carro(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveIntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)


def __str__(self):
    return "Carro:" + str(self.id)


class CarroProduto(models.Model):
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    avaliacao = models.PositiveIntegerField()
    quantidade = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    def __str__(self):
        return f"Carro: {self.carro.id}, CarroProduto: {self.id}"


PEDIDO_STATUS = (
    ("Pedido Recebido", "Pedido Recebido"),
    ("Pedido Processando", "Pedido Processando"),
    ("Pedido Caminho", "Pedido Caminho"),
    ("Pedido Completado", "Pedido Completado"),
    ("Pedido Cancelado", "Pedido Cancelado"),
)


class Pedido_order(models.Model):
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE)
    ordernar_por = models.CharField(max_length=200)
    endereco_envio = models.CharField(max_length=200)
    telefone = models.CharField(max_length=200)
    subtotal = models.PositiveIntegerField()
    disconto = models.PositiveIntegerField()
    pedido_status = models.CharField(max_length=200, choices=PEDIDO_STATUS)
    criando_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Pedido_order:" + str(self.id)


class Promocao(models.Model):
    dias = models.PositiveSmallIntegerField()
    horas = models.PositiveSmallIntegerField()
    minutos = models.PositiveSmallIntegerField()
    segundos = models.PositiveSmallIntegerField(default=0)
    imagem = models.ImageField(upload_to="promocao/",default="")

    def __str__(self):
        return f"{self.dias} dias {self.horas} horas {self.minutos} minutos {self.segundos} segundos"
