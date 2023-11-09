import time

from django.shortcuts import redirect, render
from django.views.generic import View,TemplateView
from .models import *

# Create your views here.

class Homeview(TemplateView):
    template_name = "index.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lista_produto'] = Produto.objects.all().order_by("-id")
        context['lista_promocao'] = Promocao.objects.all().order_by("-id")
        return context


class TodosProdutosView(TemplateView):
    template_name = "categorias.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lista_categorias'] = Produto.objects.all().order_by("-id")
        return context


class ProdutoDetalheView(TemplateView):
    template_name = "detalhe.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lista_produto'] = Produto.objects.all().order_by("-id")
        context['lista_promocao'] = Promocao.objects.all().order_by("-id")
        return context

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     url_slug = self.kwargs['slug']
    #     produto = Produto.objects.get(slug=url_slug)
    #     produto.visualizacao +=1
    #     produto.save()
    #     context['produto'] = produto
    #     return context

class AddCarroView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lista_produto'] = Produto.objects.all().order_by("-id")
        context['lista_promocao'] = Promocao.objects.all().order_by("-id")
        produto_id = self.kwargs['pro_id']
        produto_obj = Produto.objects.get(id=produto_id)
        carro_id = self.request.session.get("carro_id", None)


        if carro_id:
            carro_obj = Carro.objects.get(id=carro_id)
            produto_no_carro = carro_obj.carroproduto_set.filter(produto=produto_obj)

            if produto_no_carro.exists():
                carroproduto = produto_no_carro.last()
                carroproduto.quantidade += 1
                carroproduto.subtotal += produto_obj.venda
                carroproduto.save()
            else:
                carroproduto = CarroProduto.objects.create(carro=carro_obj, produto=produto_obj,
                                                           avaliacao=produto_obj.venda, quantidade=1, subtotal=produto_obj.venda)

            # Atualize o campo "total" no objeto "Carro"
            carro_obj.total = sum(item.subtotal for item in carro_obj.carroproduto_set.all())
            if carro_obj.total < 0:
                carro_obj.total = 0

            carro_obj.save()

        else:
            carro_obj = Carro.objects.create(total=produto_obj.venda)
            self.request.session['carro_id'] = carro_obj.id
            carroproduto = CarroProduto.objects.create(carro=carro_obj, produto=produto_obj,
                                                       avaliacao=produto_obj.venda, quantidade=1, subtotal=produto_obj.venda)
            carro_obj.save()


        return context


class ManipularCarroView(View):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs["cp_id"]
        acao = request.GET.get("acao")
        cp_obj = CarroProduto.objects.get(id=cp_id)

        try:
            carro_obj = cp_obj.carro
        except Carro.DoesNotExist:
            # Se o carrinho não existe, você pode criar um novo carrinho
            carro_obj = Carro.objects.create(total=0)

        if acao == "inc":
            cp_obj.quantidade += 1
            cp_obj.subtotal += cp_obj.avaliacao
            cp_obj.save()
            carro_obj.total += cp_obj.avaliacao
        elif acao == "dcr":
            if cp_obj.quantidade > 0:
                cp_obj.quantidade -= 1
                cp_obj.subtotal -= cp_obj.avaliacao
                cp_obj.save()
                carro_obj.total -= cp_obj.avaliacao
                if cp_obj.quantidade == 0:
                    cp_obj.delete()
        elif acao == "rmv":
            carro_obj.total -= cp_obj.subtotal
            cp_obj.delete()

        # Certifique-se de que o total nunca seja negativo
        if carro_obj.total < 0:
            carro_obj.total = 0
        carro_obj.save()

        return redirect("lojaapp:carrinho")



class MeuCarroView(TemplateView):
    template_name = "carrinho.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carro_id = self.request.session.get("carro_id",None)
        if carro_id:
            carro = Carro.objects.get(id=carro_id)
        else:
            carro = None
        context['carro'] = carro
        return context

class LimparCarroView(TemplateView):
    def get(self,requestm,*args,**kwargs):
        carro_id = self.request.session.get("carro_id",None)
        if carro_id:
            carro = Carro.objects.get(id=carro_id)
            carro.carroproduto_set.all().delete()
            carro.total = 0
            carro.save()
        return redirect("lojaapp:meucarro")

class ProcessarCarroView(TemplateView):
    template_name = "processar.html"
class SobreView(TemplateView):
    template_name = "sobre.html"



class ContatoView(TemplateView):
    template_name = "contato.html"

