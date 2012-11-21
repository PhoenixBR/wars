from django.shortcuts import render_to_response  # funcoes de renderizacao dos templates
from django.shortcuts import redirect  # Funcao para executar um http-redirect
from django.shortcuts import get_object_or_404  # funcao para buscar um item no banco de dados. Se nao encontrar, retorna um http 404 - page not found
from django.contrib.auth.decorators import login_required

from django.template import RequestContext

from itens.models import Arma, Armadura  # importa os modelos de armas e armaduras


@login_required
def loja(request):
    armas = Arma.objects.filter(secreta=False).order_by('compra', '-venda')
    armaduras = Armadura.objects.filter(secreta=False).order_by('compra', '-venda')
    profile = request.user.get_profile()
    return render_to_response("loja.html", {"armas": armas, "armaduras": armaduras,
                                            "profile": profile}, context_instance=RequestContext(request))


@login_required
def comprar_arma(request, nr_item):
    item = get_object_or_404(Arma, pk=nr_item)
    profile = request.user.get_profile()

    if profile.carteira >= item.compra:
        profile.carteira -= item.compra
        profile.armas.add(item)
        profile.save()

    return redirect(loja)


@login_required
def vender_arma(request, nr_item):
    item = get_object_or_404(Arma, pk=nr_item)
    profile = request.user.get_profile()

    profile.carteira += item.venda
    profile.armas.remove(item)
    if profile.arma_ativa == item:
        profile.arma_ativa = None
    profile.save()

    return redirect(loja)


@login_required
def comprar_armadura(request, nr_item):
    item = get_object_or_404(Armadura, pk=nr_item)
    profile = request.user.get_profile()

    if profile.carteira >= item.compra:
        profile.carteira -= item.compra
        profile.armaduras.add(item)
        profile.save()

    return redirect(loja)


@login_required
def vender_armadura(request, nr_item):
    item = get_object_or_404(Armadura, pk=nr_item)
    profile = request.user.get_profile()

    profile.carteira += item.venda
    profile.armaduras.remove(item)
    if profile.armadura_ativa == item:
        profile.armadura_ativa = None
    profile.save()

    return redirect(loja)
