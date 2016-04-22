#coding=utf-8
import sys
reload(sys)
#python默认环境编码时ascii
sys.setdefaultencoding("utf-8")
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from tutorial.items import TutorialItem
import re
import urllib

class ImdbSpider(Spider):
    name = "imdb"
    allowed_domains = ["www.imdb.com"]
    start_urls = []

    def start_requests(self):

        file_object = open('movie_name.txt','r')

        try:
            url_head = "http://www.imdb.com/find?ref_=nv_sr_fn&q="
            for line in file_object:
                self.start_urls.append(url_head + line)
            
            for url in self.start_urls:
                yield self.make_requests_from_url(url)
        finally:
            file_object.close()
            #years_object.close()

    def parse(self, response):
        #open("test.html",'wb').write(response.body)
        
        hxs = Selector(response)
        movie_pic = hxs.xpath('id("main")/div/div[2]/table/tr[1]/td[1]/a/img/@src').extract()
        #open("movie_pic.txt", 'w').write(str(movie_pic))
        if movie_pic:
            movie_pic[0]=movie_pic[0].replace('32','182')
            movie_pic[0]=movie_pic[0].replace('44','268')
        #download pic
        item = TutorialItem()
        item['movie_picture'] = ''.join(movie_pic).strip()
        movie_name_file = open('movie_name.txt','r')
        try:
            for line in movie_name_file:
                item['movie_name'] = line.strip()
                if movie_pic:
                    #open("movie_pictt.txt", 'w').write(str(item["movie_picture"]))
                    urllib.urlretrieve(movie_pic[0].strip(),'pictures/' + line.strip() + '.jpg')
        finally:
            movie_name_file.close()
        yield item
