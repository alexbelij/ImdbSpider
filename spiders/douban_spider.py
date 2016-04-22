#coding=utf-8
import sys
reload(sys)
#python默认环境编码时ascii
sys.setdefaultencoding("utf-8")
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector#HtmlXPathSelector
from tutorial.items import TutorialItem
import re
import urllib

class DoubanSpider(Spider):
    name = "douban"
    allowed_domains = ["movie.douban.com"]#["imdb.com"]
    start_urls = []

    def start_requests(self):
        yield Request("http://www.techbrood.com/", headers={'User-Agent': "your agent string"})
        file_object = open('movie_name.txt','r')

        try:
            url_head = "http://movie.douban.com/subject_search?search_text="
            #url_head = "http://www.imdb.com/find?ref_=nv_sr_fn&q="
            for line in file_object:
                self.start_urls.append(url_head + line)
            
            for url in self.start_urls:
                yield self.make_requests_from_url(url)
        finally:
            file_object.close()
            #years_object.close()

    def parse(self, response):
        #open("test.html",'wb').write(response.body)
        #hxs = HtmlXPathSelector(response)
        hxs = Selector(response)
        movie_link = hxs.xpath('//*[@id="content"]/div/div[1]/div[2]/table[1]/tr/td[1]/a/@href').extract()
        #movie_link = hxs.select('//*[@id="content"]/div/div[1]/div[2]/table[1]/tr/td[1]/a/@href').extract()

        
        if movie_link:
            yield Request(movie_link[0],callback=self.parse_item)
        
        
    def parse_item(self,response):
        #hxs = HtmlXPathSelector(response)
        hxs = Selector(response)
        movie_picture = hxs.xpath('//*[@id="mainpic"]/a/img/@src').extract()
        #movie_picture = hxs.select('//*[@id="mainpic"]/a/img/@src').extract()
        item = TutorialItem()

        item['movie_picture'] = ''.join(movie_picture).strip()

        #用来给爬到的图片命令的，这个文件里只有一行数据，因为我会在我的main.py文件中调用scrapy爬虫，会在main.py中不断更新这个文件
        movie_id_file = open('movie_id.txt','r')
        try:
            for line in movie_id_file:
                item['movie_id'] = line.strip()
                if movie_picture:
                    print movie_picture
                    urllib.urlretrieve(movie_picture[0].strip(),'pictures\\' + line.strip() + '.jpg')
        finally:
            movie_id_file.close()


        yield item
