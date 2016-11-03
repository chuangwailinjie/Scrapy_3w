import scrapy
from scrapy.linkextractors import LinkExtractor
from douban.items import CsdnItem

class CsdnSpider(scrapy.Spider):
	name='csdn'
	allowed_domains=['blog.csdn.net']
	start_urls=['http://blog.csdn.net/peihaozhu/article/list/1']

	def parse(self,response):
		for info in response.xpath('//dl[@class="list_c clearfix"]/dd'):
			item=CsdnItem()
			item['title'] = info.xpath('h3/a/text()').extract()
			item['url'] = info.xpath('h3/a/@href').extract()
			item['description'] = info.xpath('p[@class="list_c_c"]/text()').extract()
			item['viewpoint']=info.xpath('div[@class="list_c_b"]/div[@class="list_c_b_l"]/span[1]/text()').extract()
			yield item
		next_page = response.xpath('//div[@class="pagelist"]/a[text()="下一页"]/@href')
		if next_page:
			url = 'http://blog.csdn.net'+next_page[0].extract()
			yield scrapy.Request(url, self.parse)