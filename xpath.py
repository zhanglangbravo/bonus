#! /usr/bin/env python
# -*- coding: utf-8 -*-
#以豆瓣top250排行榜为例
import requests             #与浏览器交互
from lxml import etree   #主要用来处理xpath
import json                     #处理收集的数据


def run(num=0):
    url = 'https://movie.douban.com/top250?start={}&filter='                    #主要url，每一页主要改变的是start值
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}                                                    #headers必须要，让我们更像一个浏览器在访问，而不是爬虫
    response = requests.get(url.format(num),headers=headers)
    html_str = response.content.decode()

    html = etree.HTML(html_str)                                                                     #获取主element
    group_list = html.xpath("//ol[@class='grid_view']/li")                            #获取主路径，也就是每个电影模块并列排序的路径，好用来for循环
    for table in group_list:                                                                                #遍历每个电影，每个table都是一个类
        item = {}                                                                                                   #建立一个字典来装数据
        item['title'] = table.xpath(".//span[@class='title']/text()")[0] if len(table.xpath(".//span[@class='title']/text()")) > 0 else None           #在主路径的基础上，获取想要的信息，这里主要用到xpath语法，获取到的数据根据情况要进行修饰加工
        item['director'] = table.xpath(".//div[@class='bd']/p/text()")[0].strip().split(' ')[1]
        item['subject'] = table.xpath(".//p[@class='quote']/span/text()")
        item['star'] = table.xpath(".//div[@class='star']/span[@class='rating_num']/text()")
        with open('top250','a', encoding='utf-8') as f:                                     #将内容用追加的方式写进一个文件
            f.write(json.dumps(item,ensure_ascii=False))                                #因为写入文件的只能是字符串，需要将字典转化为json格式，并且需要去掉ascii码，使用中文支持的utf-8
            f.write('\n')

if __name__ == '__main__':
    # for i in range(0,1):                                                                           #start从0开始，到225结束，每隔25取一次
    for i in range(0,226,25):                                                                           #start从0开始，到225结束，每隔25取一次
        run(i)
