# -*- coding: utf-8 -*-
import math
import re

import requests
import pandas as pd
import time

class Car_home_class():
    '''汽车之家'''

    def __init__(self):
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
            "Referer": "https://car.autohome.com.cn/price/list-0-0-0-0-0-0-0-701-0-0-0-0-0-0-0-1.html",
        }

    def get_data(self, page=1):
        '''请求接口'''
        url = f"https://car.autohome.com.cn/price/list-0-0-0-0-0-0-0-701-0-0-0-0-0-0-0-{page}.html"
        res = requests.get(url=url, headers=self.header).text
        # print(res)
        # 返回数据
        if '用户评分' in res:
            return res
        else:
            return ""

    def data_deal(self, data_text=None):
        '''数据解析'''
        new_list = []
        # 详情链接+车名
        url_name_li = re.findall(r'<a href="/price/series-(\d+).html#pvareaid=(\d+)" target="_self" class="font-bold">(.*?)</a>', data_text)
        # 用户评分
        score_number_li = re.findall(r'<span class="score-number">(.*?)</span>', data_text)
        # 级别
        info_gray_li = re.findall(r'别：<span class="info-gray">(.*?)</span>', data_text)
        # 官方指导价
        price_li = re.findall(r'指导价：<span class="lever-price red"><span class="font-arial">(.*?)</span>', data_text)
        for i in range(len(url_name_li)):
            url_id1, url_id2, car_name = url_name_li[i]
            # 详情链接
            info_url = f'https://car.autohome.com.cn/price/series-{url_id1}.html#pvareaid={url_id2}'
            # 用户评分
            score_number = score_number_li[i]
            # 级别
            info_gray = info_gray_li[i]
            # 官方指导价
            price = price_li[i]
            new_list.append([car_name, info_url, score_number, info_gray, price])
        return new_list

    def data_to_csv(self, data_li=None):
        '''数据存储'''
        df = pd.DataFrame(data_li)
        df.to_csv("test2.csv", index=False)

    def run(self):
        # 翻页获取数据
        all_list = []
        all_list.append(["车名", "详情链接", "用户评分", "级别", "官方指导价"])
        # 爬取10页
        for page in range(1, 10):
            print("当前页数：", page)
            data_text = self.get_data(page=page)
            out_date = self.data_deal(data_text=data_text)
            print("*" * 100)
            print(out_date)
            all_list += out_date
            self.data_to_csv(data_li=all_list)
            time.sleep(3)

if __name__ == '__main__':
    ddc = Car_home_class()
    ddc.run()