
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'wars.settings'

from player.models import Player

def atualizar():
	jogadores = Player.objects.all()
	for jogador in jogadores:
		jogador.refresh()
		jogador.save()
	

atualizar()
