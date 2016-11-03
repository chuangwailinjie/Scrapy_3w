#from scrapy.selector import Selector
from scrapy.http import Request, FormRequest
from douban.items import ZhihuAnswerItem
import scrapy,json,re
#from scrapy.spiders import CrawlSpider, Rule
from lxml import etree
#from scrapy.linkextractors import LinkExtractor


'''
平时在parse中return item即可返回item，return request则生成新的request请求。如果我们将return换为yield的话即可既返回item又生成新的request。注意一旦使用了yield，那么parse方法中就不能有return了。
'''
class ZhihuSipder(scrapy.Spider) :
	name = "zhihuanswer"
	#allowed_domains = ["zhihu.com"]
	start_urls = [
		"https://www.zhihu.com"
	]
	headers = {
	"Accept": "*/*",
	"Accept-Encoding": "gzip,deflate",
	"Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
	"Connection": "keep-alive",
	"Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
	"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
	"Referer": "http://www.zhihu.com/"
	}

	xsrf=""
	moreinfo=False
	count=0

    #重写  爬虫类的方法, 实现了自定义请求, 运行成功后会调用callback回调函数  此方法是scrapy爬虫默认的获取起始爬虫方法，这里用来做转到登录
	def start_requests(self):
		return [Request("https://www.zhihu.com/#signin", meta = {'cookiejar' : 1}, callback = self.post_login)]

    #FormRequeset出问题了
	def post_login(self, response):
		print('Preparing login')
		#下面这句话用于抓取请求网页后返回网页中的_xsrf字段的文字, 用于成功提交表单
		self.xsrf = Selector(response).xpath('//input[@name="_xsrf"]/@value').extract()[0]
		print(self.xsrf)
        #FormRequeset.from_response是Scrapy提供的一个函数, 用于post表单
        #登陆成功后, 会调用after_login回调函数
		return [FormRequest(url="https://www.zhihu.com/login/email",
							meta = {'cookiejar' : response.meta['cookiejar']},
							formdata = {
							'_xsrf': self.xsrf,
							'email': '******',
							'password': '******',
							'remember_me': 'true'
							},
							headers=self.headers,
							callback = self.after_login,
							dont_filter = True
							)]

	def after_login(self, response):
		print(response.body)
		self.headers['X-Xsrftoken']=self.xsrf
		self.headers['X-Requested-With']="XMLHttpRequest"
		#for url in self.start_urls:
			#yield self.make_requests_from_url(url)#如果不重写的话，调用时默认会返回一个request，同时执行parse方法，所以这里直接用Scrapy.Request
			#yield self.make_requests_from_url(url)
		return Request('https://www.zhihu.com',meta = {'cookiejar' : response.meta['cookiejar']}, callback =self.parse,dont_filter = True)

	def parse(self, response):
		if self.moreinfo:
			f=json.loads(response.body.decode('utf-8'))
			for item in range(1,len(f['msg'])-1):
				f['msg'][0]=f['msg'][0]+f['msg'][item]
			fs=f['msg'][0].encode('utf-8')
			response._set_body(fs)
		else:
			self.moreinfo=True
		html=etree.HTML(response.body.decode('utf-8'),parser=etree.HTMLParser(encoding='utf-8'))
		for p in html.xpath('//div[@class="feed-main"]'):
			url=p.xpath('div[2]/h2[@class="feed-title"]/a/@href')
			if url:url=url[0]
			if re.findall('zhuanlan',url):continue
			item = ZhihuAnswerItem()
			item['url'] = url
			name=p.xpath('div[2]/div[@class="expandable entry-body"]/div[@class="zm-item-answer-author-info"]/span/span/a/text()')
			item['name'] = name if name else '匿名用户'
			item['question'] = p.xpath('div[2]/h2[@class="feed-title"]/a/text()')
			item['answer']= p.xpath('div[2]/div[@class="expandable entry-body"]/div[@class="zm-item-rich-text expandable js-collapse-body"]/div[@class="zh-summary summary clearfix"]/text()')
			yield item
		self.count=self.count+1
		yield FormRequest(url="https://www.zhihu.com/node/TopStory2FeedList",
							meta = {'cookiejar' : response.meta['cookiejar']},
							formdata = {
							'params': '{"offset":%d,"start":%s}' % (self.count*10,str(self.count*10-1)),
							'method': 'next',
							},
							headers=self.headers,
							callback = self.parse,
							dont_filter = True
							)