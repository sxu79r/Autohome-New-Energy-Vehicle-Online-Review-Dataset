import re
from tqdm import tqdm
import requests
import pandas as pd
import time

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
    "Referer": "https://car.autohome.com.cn/price/list-0-0-0-0-0-0-0-701-0-0-0-0-0-0-0-1.html",
}
def get_data(page):
    '''请求接口'''
    url = f"https://car.autohome.com.cn/price/list-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-{page}.html"
    res = requests.get(url=url, headers=header).text

    # print(res)
    # 返回数据
    if '用户评分' in res:
        return res
    else:
        return ""
def data_to_csv(data_li):
    '''数据存储'''
    df = pd.DataFrame(data_li)
    df.to_csv("数据集网址.csv", index=False)
def data_deal(data_text):
    '''数据解析'''
    new_list = []
    # 详情链接+车名
    url_name_li = re.findall(r'href="/price/series-(\d+?).html#pvareaid=(\d+?)" target="_self" class="font-bold">(.*?)</a>', data_text)
    for i in range(len(url_name_li)):
        url_id1, url_id2, car_name = url_name_li[i]
        # 详情链接
        info_url = f'https://car.autohome.com.cn/price/series-{url_id1}.html#pvareaid={url_id2}'
        res1 = requests.get(url=info_url, headers=header).text
        # print(res1)
        pinpai = re.findall(r'<h2 class="fn-left cartab-title-name"><a class="font-16" href="/price/brand-(\d+?).html"  target="_blank">(.*?)</a></h2>', res1)
        pinpai1, pinpai2 = pinpai[0]
        # print(pinpai2)
        # print(pinpai)
        new_list.append([pinpai2, car_name, url_id1])
    return new_list

def run():
    # 翻页获取数据
    all_list = []
    all_list.append(["品牌", "车名", "详情链接的代号"])
    # 爬取10页
    for page in tqdm(range(1, 50)):
        print("当前页数：", page)
        data_text = get_data(page)
        url_name_li = re.findall(
r'href="/price/series-(\d+?).html#pvareaid=(\d+?)" target="_self" class="font-bold">(.*?)</a>', data_text)
        out_date = data_deal(data_text)
        print("*" * 100)
        print(out_date)
        all_list += out_date
        data_to_csv(all_list)
        time.sleep(3)
if __name__ == '__main__':
    run()