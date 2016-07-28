# -*- coding: utf-8 -*-

from scrapy.item import Item, Field

class AnimeItem(Item):
    titulo = Field()
    link = Field()
    extras = Field()
    
class ContenidoItem(Item):
	titulo = Field()
	# cont = Field()
	# imagen = Field()
	# capitulos = Field()
	link = Field()
