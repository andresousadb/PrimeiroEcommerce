from django.urls import path
from .views import *

app_name = "lojaapp"

urlpatterns = [
    path("", Homeview.as_view(), name="index"),
    path("sobre/", SobreView.as_view(), name="sobre"),
    path("contato/", ContatoView.as_view(), name="contato"),
    path("todos-produtos/", TodosProdutosView.as_view(), name="categorias"),
    path('Produto/', ProdutoDetalheView.as_view(), name='detalhe'),

    path("addcarro/<int:pro_id>/", AddCarroView.as_view(), name='addcarro'),

    path("meu-carro/", MeuCarroView.as_view(), name='carrinho'),
    path("manipular-carro/<int:cp_id>/", ManipularCarroView.as_view(), name='manipularcarro'),
    path("limpar-carro/", LimparCarroView.as_view(), name='limparcarro'),
    path("processar-carro/", ProcessarCarroView.as_view(), name='processar'),
]

