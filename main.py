#coding=utf-8
import sys
reload(sys)
#python默认环境编码时ascii
sys.setdefaultencoding("utf-8")

import os
import csv
#read csv
csvfile = file('F:/moviespd/movie2011.csv','r')
reader = csv.reader(csvfile)
movie_nm = []

for line in reader:
    if line[0] != '' and line[0]!='Film' and line[0]!= 'Average':
        movie_nm.append(line[0])    
csvfile.close()

#读取电影数据
try:
    for x in movie_nm:
        #数据整理
        movie_title = x #movie_infos[2]
        #print movie_id + ":" + movie_title
        write_name = movie_title.replace('_','+')
        write_name = write_name.replace('\'','')
        write_name = write_name.replace(':', '%3A')
        if write_name.find('(')!= -1:
            write_name = write_name[:write_name.find('(')]
        #print "name is :" + write_name
        
        #把电影名写到中间文件中去，让爬虫读取
        movie_name_file = open('movie_name.txt','w')
        try:
            movie_name_file.write(write_name)
        finally:
            movie_name_file.close()

        #该爬虫程序会从movie_name中读取电影名来爬虫
        os.system(r"scrapy crawl imdb")

finally:
    print "finished crawl"
    #movies_info.close()
