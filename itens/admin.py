# importamos o modulo de admin
from django.contrib import admin
 
# importamos os modelos desta app que desejamos que o django-admin administre
from itens.models import Arma, Armadura
from player.models import Player
 
class ItensAdmin(admin.ModelAdmin):
	list_display = ('nome', 'poder', 'compra', 'venda')
	

 
class PlayerAdmin(admin.ModelAdmin):
	list_display = ('user','carteira','banco', 'ataque', 'defesa', 'vida', 'energia','raiva','hp','energia_atual','raiva_atual','nivel','experiencia','pontos','arma_ativa','armadura_ativa')
 
#cadastramos o modelo das armas no django-admin
admin.site.register(Player, PlayerAdmin)
 
#cadastramos o modelo das armas no django-admin
admin.site.register(Arma, ItensAdmin)
 
#cadastramos o modelo das armaduras no django-admin
admin.site.register(Armadura, ItensAdmin)