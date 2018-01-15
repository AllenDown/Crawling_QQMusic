#! /usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import database
import time

singer_list = database.get_sheet('QQMusic', 'singer_list')
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                    '41.0.2272.118 Safari/537.36',
       'referer': 'https://y.qq.com/portal/singer_list.html'
       }

url = 'https://c.y.qq.com/v8/fcg-bin/v8.fcg?channel=singer&page=list&key=all_all_all&pagesize=100&pagenum={}&g_tk=1445151743&jsonpCallback=GetSingerListCallback&loginUin=707813012&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'
urls = [url.format(i) for i in range(1, 5527)]

# get all singers in one page and insert into database
def get_singers(url):
    print('crawling url : ' + url)
    web_data = ''
    while web_data == '':
        try:
            web_data = requests.get(url, headers=headers)
        except:
            print('bad network, let us sleep for 5 seconds')
            print('uncrawled url : ' + url)
            time.sleep(5)
            continue
    res = json.loads(web_data.text.lstrip(" ''GetSingerListCallback('").rstrip(')'))['data']['list']
    print(res)
    if res != '':
        singer_list.insert_many(res)


