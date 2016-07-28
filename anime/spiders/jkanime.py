# -*- coding: utf-8 -*-
import scrapy
import re

from scrapy import Spider
from scrapy.selector import Selector 

from anime.items import	AnimeItem

import scrapy


re2='/(\\d+)/'	# Integer Number 1

class JkanimeSpider(scrapy.Spider):
	name = 'contenido'
	start_urls = (
		'http://jkanime.net/letra/0-9/',
		'http://jkanime.net/letra/A/',
		# 'http://jkanime.net/letra/B/',
		# 'http://jkanime.net/letra/C/',
		# 'http://jkanime.net/letra/D/',
		# 'http://jkanime.net/letra/E/',
		# 'http://jkanime.net/letra/F/',
		# 'http://jkanime.net/letra/G/',
		# 'http://jkanime.net/letra/H/',
		# 'http://jkanime.net/letra/I/',
		# 'http://jkanime.net/letra/J/',
		# 'http://jkanime.net/letra/K/',
		# 'http://jkanime.net/letra/L/',
		# 'http://jkanime.net/letra/M/',
		# 'http://jkanime.net/letra/N/',
		# 'http://jkanime.net/letra/O/',
		# 'http://jkanime.net/letra/P/',
		# 'http://jkanime.net/letra/Q/',
		# 'http://jkanime.net/letra/R/',
		# 'http://jkanime.net/letra/S/',
		# 'http://jkanime.net/letra/T/',
		# 'http://jkanime.net/letra/U/',
		# 'http://jkanime.net/letra/V/',
		# 'http://jkanime.net/letra/W/',
		# 'http://jkanime.net/letra/X/',
		# 'http://jkanime.net/letra/Y/',
		# 'http://jkanime.net/letra/Z/',
	)
	DOWNLOAD_DELAY = 0.1 

	def parse(self, response):
		for href in response.css('a.titl::attr(href)'):
			full_url = response.urljoin(href.extract())
			yield scrapy.Request(full_url, callback=self.parse_question)

	def parse_question(self, response):
		yield {
			'titulo': response.css('.sinopsis_title::text').extract_first(),
			'link': response.url,
			'idAjax': response.xpath("substring(//script[contains(.,'if (Math.round(Math.random() * (99)) == 27)')]/text(),106,6)").re(re2),
			'paginas':response.css('.listnavi .listpag').extract(),
			'cont': response.css('.sinoptext p::text').extract_first(),
			'imagen': response.css('.separedescrip img::attr(src)').extract_first(),
			'datos': { 
				'tipo': response.css('.separedescrip:nth-child(2) > div:nth-child(1) > span:nth-child(2)::text').extract_first(),
				'genero': response.css('.separedescrip:nth-child(2) > div:nth-child(2) > span:nth-child(2) a::text').extract(),
				'episodios': response.css('.separedescrip:nth-child(2) > div:nth-child(3) > span:nth-child(2)::text').extract_first(),
				'emision': response.css('.separedescrip:nth-child(2) > div:nth-child(5) > span:nth-child(2)::text').extract_first(),
				'estado': response.css('.separedescrip:nth-child(2) > div:nth-child(6) > span:nth-child(2)::text').extract_first()
			},
		}

class ListadoSpider(Spider):
	name = "listado"
	allowed_domains = ["jkanime.net"]
	start_urls = (
		'http://jkanime.net/letra/0-9/',
		'http://jkanime.net/letra/A/',
		'http://jkanime.net/letra/B/',
		'http://jkanime.net/letra/C/',
		'http://jkanime.net/letra/D/',
		'http://jkanime.net/letra/E/',
		'http://jkanime.net/letra/F/',
		'http://jkanime.net/letra/G/',
		'http://jkanime.net/letra/H/',
		'http://jkanime.net/letra/I/',
		'http://jkanime.net/letra/J/',
		'http://jkanime.net/letra/K/',
		'http://jkanime.net/letra/L/',
		'http://jkanime.net/letra/M/',
		'http://jkanime.net/letra/N/',
		'http://jkanime.net/letra/O/',
		'http://jkanime.net/letra/P/',
		'http://jkanime.net/letra/Q/',
		'http://jkanime.net/letra/R/',
		'http://jkanime.net/letra/S/',
		'http://jkanime.net/letra/T/',
		'http://jkanime.net/letra/U/',
		'http://jkanime.net/letra/V/',
		'http://jkanime.net/letra/W/',
		'http://jkanime.net/letra/X/',
		'http://jkanime.net/letra/Y/',
		'http://jkanime.net/letra/Z/',
	)

	def parse(self, response):
		lista = Selector(response).xpath('//table[@class="search"]')

		for anime in lista:
			item = AnimeItem()
			item['titulo'] = anime.xpath('tr/td[2]/a[@class="titl"]/text()').extract()
			item['link'] = anime.xpath('tr/td[2]/a[@class="titl"]/@href').extract()
			yield item

		next_page = response.xpath('.//a[@class="listsiguiente"]/@href').extract()
		if next_page:
			url = response.urljoin(next_page[0])
			yield scrapy.Request(url, self.parse)