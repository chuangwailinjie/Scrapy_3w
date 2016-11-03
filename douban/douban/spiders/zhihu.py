from scrapy.selector import Selector
from scrapy.http import Request, FormRequest
from douban.items import ZhihuItem
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


'''
平时在parse中return item即可返回item，return request则生成新的request请求。如果我们将return换为yield的话即可既返回item又生成新的request。注意一旦使用了yield，那么parse方法中就不能有return了。
'''
class ZhihuSipder(CrawlSpider) :
	name = "zhihu"
	allowed_domains = ["zhihu.com"]
	start_urls = [
		"https://www.zhihu.com/question/41472220"
	]
	rules = (
		Rule(LinkExtractor(allow = [r'/question/\d{8}$',r'https://www.zhihu.com/question/\d{8}$' ]), callback = 'parse_item', follow = True),
		#Rule(LinkExtractor(allow = ('/question/\d+', )), callback = 'self.parse_item', follow = True),
	)
	headers = {
	"Accept": "*/*",
	"Accept-Encoding": "gzip,deflate",
	"Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
	"Connection": "keep-alive",
	"Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
	"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
	"Referer": "http://www.zhihu.com/"
	}

    #重写  爬虫类的方法, 实现了自定义请求, 运行成功后会调用callback回调函数  此方法是scrapy爬虫默认的获取起始爬虫方法，这里用来做转到登录
	def start_requests(self):
		return [Request("https://www.zhihu.com/#signin", meta = {'cookiejar' : 1}, callback = self.post_login)]

    #FormRequeset出问题了
	def post_login(self, response):
		print('Preparing login')
		#下面这句话用于抓取请求网页后返回网页中的_xsrf字段的文字, 用于成功提交表单
		xsrf = Selector(response).xpath('//input[@name="_xsrf"]/@value').extract()[0]
		print(xsrf)
        #FormRequeset.from_response是Scrapy提供的一个函数, 用于post表单
        #登陆成功后, 会调用after_login回调函数
		return [FormRequest(url="https://www.zhihu.com/login/email",
							meta = {'cookiejar' : response.meta['cookiejar']},
							formdata = {
							'_xsrf': xsrf,
							'email': '****',
							'password': '*****',
							'remember_me': 'true'
							},
							headers=self.headers,
							callback = self.after_login,
							dont_filter = True
							)]

	def after_login(self, response):
		print(response.body)
		for url in self.start_urls:
			yield self.make_requests_from_url(url)#如果不重写的话，调用时默认会返回一个request，同时执行parse方法，所以这里直接用Scrapy.Request
			#yield self.make_requests_from_url(url)
		#return [Request('https://www.zhihu.com',meta = {'cookiejar' : response.meta['cookiejar']}, callback =self.parse_item,dont_filter = True)]

	def parse_item(self, response):
		problem = Selector(response)
		item = ZhihuItem()
		item['url'] = response.url
		item['name'] = problem.xpath('//span[@class="name"]/text()').extract()
		item['title'] = problem.xpath('//span[@class="zm-editable-content"]/text()').extract()
		item['description'] = problem.xpath('//div[@class="zm-editable-content"]/text()').extract()
		item['answer']= problem.xpath('//div[@class="zm-editable-content clearfix"]/text()').extract()
		return item

if __name__ == "__main__":
    from scrapy.cmdline import execute

    execute()
    print("")