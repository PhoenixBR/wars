from django.shortcuts import render_to_response # funcoes de renderizacao dos templates
from django.shortcuts import redirect # Funcao para executar um http-redirect
from django.contrib.auth.decorators import login_required

from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm # Formulario de criacao de usuarios

from player.models import Player


# pagina de cadastro de jogador
def registrar(request):
     
    # Se dados forem passados via POST
    if request.method == 'POST':
        form = UserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("pagina_inicial")
    
    else:
        form =  UserCreationForm()
    return render_to_response("registrar.html", {"form": form}, 
        context_instance=RequestContext(request))

@login_required
def malicia_grana(request):
    profile = request.user.get_profile()
    profile.carteira += 50
    profile.save()
    return redirect("pagina_inicial")

@login_required
def malicia_refresh(request):
    profile = request.user.get_profile()
    profile.refresh()
    profile.save()
    return redirect("pagina_inicial")

@login_required
def malicia_hospital(request):
    profile = request.user.get_profile()
    profile.hp = profile.vida * 10
    profile.save()
    return redirect("pagina_inicial")

@login_required
def rank(request):
    rank = Player.objects.all()[:10]
    return render_to_response("rank.html", {"rank": rank})

