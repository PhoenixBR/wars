from django.shortcuts import render_to_response # funcoes de renderizacao dos templates
from django.shortcuts import redirect # Funcao para executar um http-redirect
from django.contrib.auth.decorators import login_required

from random import randint # funcao para escolher um numero aleatorio

# pagina que lista os crimes

@login_required
def crimes(request):
    user = request.user
    profile = user.get_profile()
    experiencia_necessaria = profile.getExperiencias()
    return render_to_response("crimes.html", {"user":user, "profile": profile, "xp_necessario": experiencia_necessaria[profile.nivel+1]-profile.experiencia})

@login_required
def cometer_crime(request, crime):
 
    player = request.user.get_profile()
    
 
    if(crime=='1'):
        
        if player.energia_atual >= 1:    
            #ganha um dinheirinho aleatorio    
            player.carteira = player.carteira + randint(5,15)
            #reduz a quantidade doe energia atual do player
            player.energia_atual = player.energia_atual - 1
            player.experiencia += randint(1,5)
            player.level_up()
            player.save() #salva no banco de dados as alteracoes

    elif(crime=='2'):
         
        if player.energia_atual >= 2 and player.nivel >= 2:
            #ganha um dinheirinho aleatorio    
            player.carteira = player.carteira + randint(10,30)
            #reduz a quantidade de energia atual do player
            player.energia_atual = player.energia_atual - 2
            player.experiencia += randint(5,15)
            player.level_up()
            player.save() #salva no banco de dados as alteracoes

    elif(crime=='3'):

        if player.energia_atual >= 5 and player.nivel >= 3 and player.arma_ativa:
            #ganha um dinheirinho aleatorio    
            player.carteira = player.carteira + randint(30,75)
            #reduz a quantidade de energia atual do player
            player.energia_atual = player.energia_atual - 5
            player.experiencia += randint(15,45)
            player.level_up()
            player.save() #salva no banco de dados as alteracoes        
    
    return redirect(crimes)