from django.shortcuts import redirect, render
from django.views.generic import View, TemplateView
from .models import *


# Create your views here.

class Homeview(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lista_produto'] = Produto.objects.all().order_by("-id")
        context['lista_promocao'] = Promocao.objects.all().order_by("-id")
        return context


class AddCarroViewCategoria(TemplateView):
    template_name = "categorias.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categorias_unicas = list(set(produto.categoria for produto in Produto.objects.all().order_by("-id")))
        context['lista_produtos'] = Produto.objects.all().order_by("-id")
        context['lista_categorias'] = categorias_unicas



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
                                                           avaliacao=produto_obj.venda, quantidade=1,
                                                           subtotal=produto_obj.venda)

            # Atualize o campo "total" no objeto "Carro"
            carro_obj.total = sum(item.subtotal for item in carro_obj.carroproduto_set.all())
            if carro_obj.total < 0:
                carro_obj.total = 0

            carro_obj.save()

        else:
            carro_obj = Carro.objects.create(total=produto_obj.venda)
            self.request.session['carro_id'] = carro_obj.id
            carroproduto = CarroProduto.objects.create(carro=carro_obj, produto=produto_obj,
                                                       avaliacao=produto_obj.venda, quantidade=1,
                                                       subtotal=produto_obj.venda)
            carro_obj.save()

        return context



class TodosProdutosView(TemplateView):
    template_name = "categorias.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtém a categoria selecionada do filtro, se houver
        categoria_selecionada = self.request.GET.get('categoria', None)
        print("Categoria Selecionada:", categoria_selecionada)

        # Obtém todas as categorias únicas ordenadas por id
        categorias_unicas = list(set(produto.categoria for produto in Produto.objects.all().order_by("-id")))

        # Inicializa um dicionário para armazenar o total de produtos por categoria
        total_produtos_por_categoria = {}

        # Obtém todos os produtos
        lista_produtos = Produto.objects.all().order_by("-id")

        # Se uma categoria foi selecionada no filtro, filtra a lista de produtos
        if categoria_selecionada:
            lista_produtos_filtrados = lista_produtos.filter(categoria__titulo=categoria_selecionada)
            total_produtos_por_categoria[categoria_selecionada] = lista_produtos_filtrados.count()
        else:
            # Caso contrário, obtém a contagem para todas as categorias
            for categoria in categorias_unicas:
                produtos_por_categoria = lista_produtos.filter(categoria__titulo=categoria.titulo)
                total_produtos_por_categoria[categoria.titulo] = produtos_por_categoria.count()

        # Adiciona a lista de produtos, categorias e o total de produtos por categoria ao contexto
        context['lista_produtos'] = lista_produtos
        context['lista_categorias'] = categorias_unicas
        context['total_produtos_por_categoria'] = total_produtos_por_categoria

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
                                                           avaliacao=produto_obj.venda, quantidade=1,
                                                           subtotal=produto_obj.venda)

            # Atualize o campo "total" no objeto "Carro"
            carro_obj.total = sum(item.subtotal for item in carro_obj.carroproduto_set.all())
            if carro_obj.total < 0:
                carro_obj.total = 0

            carro_obj.save()

        else:
            carro_obj = Carro.objects.create(total=produto_obj.venda)
            self.request.session['carro_id'] = carro_obj.id
            carroproduto = CarroProduto.objects.create(carro=carro_obj, produto=produto_obj,
                                                       avaliacao=produto_obj.venda, quantidade=1,
                                                       subtotal=produto_obj.venda)
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
        carro_id = self.request.session.get("carro_id", None)
        if carro_id:
            carro = Carro.objects.get(id=carro_id)
        else:
            carro = None
        context['carro'] = carro
        return context


class LimparCarroView(TemplateView):
    def get(self, requestm, *args, **kwargs):
        carro_id = self.request.session.get("carro_id", None)
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
