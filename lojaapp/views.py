from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import View, TemplateView
from .models import *


# Create your views here.


class Homeview(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lista_produto"] = Produto.objects.all().order_by("-id")
        context["lista_promocao"] = Promocao.objects.all().order_by("-id")
        return context


class AddCarroViewCategoria(TemplateView):
    template_name = "categorias.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categorias_unicas = list(
            set(produto.categoria for produto in Produto.objects.all().order_by("-id"))
        )
        context["lista_produtos"] = Produto.objects.all().order_by("-id")
        context["lista_categorias"] = categorias_unicas

        produto_id = self.kwargs["pro_id"]
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
                carroproduto = CarroProduto.objects.create(
                    carro=carro_obj,
                    produto=produto_obj,
                    avaliacao=produto_obj.venda,
                    quantidade=1,
                    subtotal=produto_obj.venda,
                )

            # Atualize o campo "total" no objeto "Carro"
            carro_obj.total = sum(
                item.subtotal for item in carro_obj.carroproduto_set.all()
            )
            if carro_obj.total < 0:
                carro_obj.total = 0

            carro_obj.save()

        else:
            carro_obj = Carro.objects.create(total=produto_obj.venda)
            self.request.session["carro_id"] = carro_obj.id
            carroproduto = CarroProduto.objects.create(
                carro=carro_obj,
                produto=produto_obj,
                avaliacao=produto_obj.venda,
                quantidade=1,
                subtotal=produto_obj.venda,
            )
            carro_obj.save()

        return context


class TodosProdutosView(TemplateView):
    template_name = "categorias.html"
    produtos_por_pagina = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categorias_filtradas = self.request.GET.get("categoria")
        categorias_unicas = list(
            set(
                produto.categoria.titulo
                for produto in Produto.objects.all().order_by("-id")
            )
        )

        lista_produtos = Produto.objects.all().order_by("-id")

        if categorias_filtradas:
            categorias_filtradas = categorias_filtradas.split(
                ","
            )  # Divide as categorias por vírgula
            categoria_objs = Categoria.objects.filter(titulo__in=categorias_filtradas)
            lista_produtos = lista_produtos.filter(
                categoria__in=categoria_objs
            ).order_by("-id")

        paginator = Paginator(lista_produtos, self.produtos_por_pagina)
        page = self.request.GET.get("page", 1)

        try:
            produtos_paginados = paginator.page(page)
        except EmptyPage:
            produtos_paginados = paginator.page(1)

        context["lista_produtos"] = produtos_paginados
        context["lista_categorias"] = categorias_unicas
        context["categorias_filtradas"] = categorias_filtradas
        context["total_produtos"] = lista_produtos.count()

        # Adiciona o parâmetro de filtro à URL da próxima página
        base_url = (
            f"?categoria={'&categoria='.join(categorias_filtradas)}"
            if categorias_filtradas
            else ""
        )
        next_page_number = (
            produtos_paginados.next_page_number()
            if produtos_paginados.has_next()
            else None
        )

        # Verifica se há produtos suficientes para preencher a próxima página
        if (
            next_page_number
            and (produtos_paginados.number * self.produtos_por_pagina)
            < lista_produtos.count()
        ):
            context["next_page_url"] = f"{base_url}&page={next_page_number}"
        else:
            context["next_page_url"] = None

        return context


class ProdutoDetalheView(TemplateView):
    template_name = "detalhe.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lista_produto"] = Produto.objects.all().order_by("-id")
        context["lista_promocao"] = Promocao.objects.all().order_by("-id")
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
        context["lista_produto"] = Produto.objects.all().order_by("-id")
        context["lista_promocao"] = Promocao.objects.all().order_by("-id")
        produto_id = self.kwargs["pro_id"]
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
                carroproduto = CarroProduto.objects.create(
                    carro=carro_obj,
                    produto=produto_obj,
                    avaliacao=produto_obj.venda,
                    quantidade=1,
                    subtotal=produto_obj.venda,
                )

            # Atualize o campo "total" no objeto "Carro"
            carro_obj.total = sum(
                item.subtotal for item in carro_obj.carroproduto_set.all()
            )
            if carro_obj.total < 0:
                carro_obj.total = 0

            carro_obj.save()

        else:
            carro_obj = Carro.objects.create(total=produto_obj.venda)
            self.request.session["carro_id"] = carro_obj.id
            carroproduto = CarroProduto.objects.create(
                carro=carro_obj,
                produto=produto_obj,
                avaliacao=produto_obj.venda,
                quantidade=1,
                subtotal=produto_obj.venda,
            )
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
        context["carro"] = carro
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
