# Create your views here.
from django.shortcuts import render_to_response # funcoes de renderizacao dos templates
from django.shortcuts import redirect # Funcao para executar um http-redirect
from django.shortcuts import get_object_or_404 # funcao para buscar um item no banco de dados. Se nao encontrar, retorna um http 404 - page not found

from player.models import Player # precisamos para listar os alvos
from django.contrib.auth.decorators import login_required

from random import randint

# pagina que lista os possiveis alvos
@login_required
def alvos(request):  
    #da um refresh no hp, energia e raiva do player
    jogador = request.user.get_profile()
    jogador.refresh()
    jogador.save()

    #pega os alvos
    # jogadores que estejam no range entre 60% e 140% da xp do jogador
    # nao pode ser o nosso jogador
    # nao pode ser um jogador com 0 de experiencia
    # nao pode ser um jogador morto. hp = 0
    # pega apenas 10
    # quem me deu a dica de como aninhar varios filtros de forma elegante, de acordo com a PEP-8 foi o Renato Oliveira <http://www.labcodes.com.br/>
    alvos = Player.objects.filter(
        experiencia__gte = (jogador.experiencia * 0.6)
    ).filter(
        experiencia__lte = (jogador.experiencia * 1.4)
    ).exclude(
        id = jogador.id
    ).exclude(
        experiencia = 0
    ).exclude(
        hp = 0
    )

    return render_to_response("alvo.html", { "nome_jogador": request.user.username,
                                             "player": jogador,
                                             "vida": jogador.vida * 10,
                                             "alvos": alvos})

#view da luta
@login_required
def atacar(request, alvo_id):     
     
    #verifica se esta sendo passado um alvo valido
    alvo = get_object_or_404(Player, pk=alvo_id)
     
    #pega o nosso jogador da sessao
    jogador = request.user.get_profile()
     
     
    #verifica se a experiencia do alvo eh menor que 60% da experiencia do atacante
    if jogador.experiencia * 0.6 > alvo.experiencia:
        return redirect(alvos)
     
     
    #atualiza o alvo e o jogador
    alvo.refresh()
    jogador.refresh()
     
     
    #verifica se o nosso jogador possui raiva para atacar
    if jogador.raiva_atual <= 0:
        return redirect(alvos)
     
     
    #verifica se o nosso jogador esta "morto"
    if jogador.hp <= 0:
        return redirect(alvos)
     
    #verifica se o alvo esta 'morto'
    if alvo.hp <= 0:
        return redirect(alvos)
     
     
    #salva o hp inicial do jogador e do alvo para fazer um pequeno relatorio no final
    jogador_hp = jogador.hp
    alvo_hp = alvo.hp
     
     
    #pega o valor da arma do jogador
    if jogador.arma_ativa:
        jogador_arma = jogador.arma_ativa.poder
    else:
        jogador_arma = 1
     
    #pega o valor da armadura do jogador
    if jogador.armadura_ativa:
        jogador_armadura = jogador.armadura_ativa.poder
    else:
        jogador_armadura = 1
     
     
    #pega o valor da arma do alvo
    if alvo.arma_ativa:
        alvo_arma = alvo.arma_ativa.poder
    else:
        alvo_arma = 1
     
    #pega o valor da armadura do alvo
    if alvo.armadura_ativa:
        alvo_armadura = alvo.armadura_ativa.poder
    else:
        alvo_armadura = 1
     
     
    luta_Log = {}
    #agora o bicho vai pegar!
    #a luta dura 3 turnos
    for turno in [1, 2, 3]:
        #primeiro o jogador ataca
        ataque_jogador = randint(jogador.ataque/3, jogador.ataque)
        defesa_alvo = randint(alvo.defesa/3, alvo.defesa)
         
        #calcula o dano
        dano_jogador = ataque_jogador * jogador_arma - defesa_alvo * alvo_armadura
         
        if dano_jogador > 0:
            alvo.hp = alvo.hp - dano_jogador
         
         
        #agora o alvo ataca
        ataque_alvo = randint(alvo.ataque/3, alvo.ataque)
        defesa_jogador = randint(jogador.defesa/3, jogador.defesa)
         
        #calcula o dano
        dano_alvo = ataque_alvo * alvo_arma - defesa_jogador * jogador_armadura
         
        if dano_alvo > 0:
            jogador.hp = jogador.hp - dano_alvo
         
        
        luta_Log[turno] = (ataque_jogador,defesa_alvo,dano_jogador,ataque_alvo,defesa_jogador,dano_alvo)
        #verifica se alguem morreu no combate
        if jogador.hp <= 0 or alvo.hp <= 0:
            break
     
     
    #descobrindo quem perdeu
    print luta_Log
    print jogador.hp
    print alvo.hp
    print (alvo_hp - alvo.hp)
    print (jogador_hp - jogador.hp)
    if jogador.hp < 0:
        vitoria = False
    elif alvo.hp < 0:
        vitoria = True
    elif (alvo_hp - alvo.hp) < (jogador_hp - jogador.hp):
        vitoria = False
    else:
        vitoria = True
    print
     
    #se o jogador ganhou, tira dinheiro do alvo e da ao jogador
    if vitoria:
        grana = alvo.carteira * ( randint(10, 90)/100.0 ) #entre 10% e 90% do valor da carteira
        grana = round(grana)
         
        alvo.carteira = alvo.carteira - grana
        jogador.carteira = jogador.carteira + grana
         
        #ganha 10% da experiencia do adversario
        jogador.experiencia = jogador.experiencia + alvo.experiencia * 0.1
    else:
        grana = jogador.carteira * ( randint(10, 90)/100.0 ) #entre 10% e 90% do valor da carteira
        grana = round(grana)
         
        alvo.carteira = alvo.carteira + grana
        jogador.carteira = jogador.carteira - grana
         
        #ganha 10% da experiencia do adversario
        alvo.experiencia = alvo.experiencia + jogador.experiencia * 0.1
     
     
    # o nosso atacante perde 1 de raiva
    jogador.raiva_atual = jogador.raiva_atual - 1
     
     
    #verifica se alguem deu level up
    jogador_hp_final = jogador.hp
    alvo_hp_final = alvo.hp

    alvo.level_up()
    jogador.level_up()
     
     
    #salva todas as alteracoes no banco de dados
    alvo.save()
    jogador.save()
     
     
    #exibe o template com o resultado da luta
    return render_to_response("atacar.html", {"player": jogador,
                                              "vida": jogador.vida * 10,
                                              "alvo": alvo,
                                              "vitoria": vitoria,
                                              "grana": grana,
                                              "jogador_hp": jogador_hp,
                                              "alvo_hp": alvo_hp,
                                              "jogador_hp_final": jogador_hp_final,
                                              "alvo_hp_final": alvo_hp_final,
                                              "log": luta_Log})