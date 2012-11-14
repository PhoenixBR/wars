from django.shortcuts import render_to_response # funcoes de renderizacao dos templates
from django.shortcuts import redirect # Funcao para executar um http-redirect
from django.shortcuts import get_object_or_404 # funcao para buscar um item no banco de dados. Se nao encontrar, retorna um http 404 - page not found
from django.contrib.auth.decorators import login_required

from itens.models import Arma, Armadura #importa os modelos de armas e armaduras

# pagina inicial do projeto django-wars
@login_required
def index(request):
    user = request.user
    user_profile = user.get_profile()
    return render_to_response("index.html", {"user":user, "profile": user_profile})
 
@login_required
def equipar_arma(request, nr_item):
    
    item = get_object_or_404(Arma, pk=nr_item)
    player = request.user.get_profile()
    if item in player.armas.all():
        player.arma_ativa = item
        player.save()
    return redirect(index)

@login_required
def equipar_armadura(request, nr_item):
    
    item = get_object_or_404(Armadura, pk=nr_item)
    player = request.user.get_profile()
    if item in player.armaduras.all():
        player.armadura_ativa = item
        player.save()
    return redirect(index)

@login_required
def adicionarStatus(request, status):
    profile = request.user.get_profile()
    if profile.pontos>=1:
        umDesses = True
        if status.lower()=='ataque':
            profile.ataque += 1
        elif status.lower()=='defesa':
            profile.defesa += 1
        elif status.lower()=='vida':
            profile.vida += 1
        elif status.lower()=='energia':
            profile.energia += 1
        elif status.lower()=='raiva':
            profile.raiva += 1
        else:
            umDesses = False

        if umDesses:
            profile.pontos -= 1
            profile.save()

    return redirect(index)

# def refresh_user(fn):
#     jogador = request.user.get_profile()
#     jogador.refresh()
#     jogador.save()
#     return fn