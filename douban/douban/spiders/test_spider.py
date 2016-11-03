import scrapy
from douban.items import DoubanItem
class TestSpider(scrapy.Spider):
	name='test'
	allowed_domains=['dmoz.org']
	start_urls=[
		"http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
	]

	def parse(self,response):
		for sel in response.xpath('//ul/li'):
			item=DoubanItem()
			item['name']=sel.xpath('a/text()').extract()
			item['url']=sel.xpath('a/@href').extract()
			item['description']=sel.xpath('text()').extract()
			yield item