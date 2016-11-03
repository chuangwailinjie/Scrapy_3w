from scrapy.selector import Selector
from douban.items import CnBlogItem
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


'''
平时在parse中return item即可返回item，return request则生成新的request请求。如果我们将return换为yield的话即可既返回item又生成新的request。注意一旦使用了yield，那么parse方法中就不能有return了。
'''
class CnBlogSipder(CrawlSpider) :
	name = "cnblog"   #设置爬虫名称

	allowed_domains = ["blog.csdn.net"] 
	start_urls = [
	    "http://blog.csdn.net/peihaozhu/article/list/1", 
	]
 
 
	rules = (
		Rule(LinkExtractor(allow=('/peihaozhu/article/list/\d+', ),),callback='parse_item',follow=True),
	)  #制定规则
 
 
	def parse_item(self, response):
		sel = response.selector
		posts = sel.xpath('//dl[@class="list_c clearfix"]/dd')
		items = []
		for p in posts:
			#content = p.extract()
			#self.file.write(content.encode("utf-8"))
			item = CnBlogItem()
			item["title"] = p.xpath('h3[@class="list_c_t"]/a/text()').extract()
			item["url"] = p.xpath('h3[@class="list_c_t"]/a/@href').extract()
			item['description']= p.xpath('p[@class="list_c_c"]/text()').extract()
			items.append(item)

		return items