import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from douban.items import DoubanItem

class DoubanSpider(scrapy.Spider):
	name='douban'
	allowed_domains=['movie.douban.com']
	start_urls=['https://movie.douban.com/top250?start=0&filter=']

	def parse(self,response):
		for info in response.xpath('//div[@class="item"]'):
			item=DoubanItem()
			item['name'] = info.xpath('div[@class="pic"]/a/img/@alt').extract()
			item['url'] = info.xpath('div[@class="pic"]/a/@href').extract()
			item['description'] = info.xpath('div[@class="info"]/div[@class="bd"]/p[@class="quote"]/span/text()').extract()
			yield item
		next_page = response.xpath('//span[@class="next"]/a/@href')
		if next_page:
			url = response.urljoin(next_page[0].extract())
			yield scrapy.Request(url, self.parse)