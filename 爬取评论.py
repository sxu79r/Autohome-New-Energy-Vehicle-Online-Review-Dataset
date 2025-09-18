import re

import requests
import pandas as pd
import time
from selenium import webdriver
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
    "Referer": "https://car.autohome.com.cn/price/list-0-0-0-0-0-0-0-701-0-0-0-0-0-0-0-1.html",
}
def get_data(id,page):
    '''请求接口'''
    # url = f"https://k.autohome.com.cn/{id}/index_{page}.html?#listcontainer"
    # res = requests.get(url=url, headers=header).text

    # 创建一个浏览器实例
    driver = webdriver.Chrome()

    # 打开目标网页
    driver.get(f"https://k.autohome.com.cn/{id}/index_{page}.html?order=0#listcontainer")

    # 获取渲染后的页面内容
    page_content = driver.page_source
    # print(page_content)
    # 关闭浏览器实例
    driver.quit()

    # print(res)
    # 返回数据
    # if '用户评分' in res:
    #     return res
    # else:
    #     return ""
    return page_content
def data_to_csv(data_li):
    '''数据存储'''
    df = pd.DataFrame(data_li)
    df.to_csv("评论004.csv", index=False)
def data_deal(pinpai,data_text):
    '''数据解析'''
    new_list = []
    # 详情链接+车名
    url_name_li = re.findall(r'href="https://k.autohome.com.cn/detail/(.*?).html#pvareaid=(\d+)" rel="noreferrer">查看完整口碑<i class="list_arrow_right__EtpQA list_icon__aL4pn"><.i><.a>', data_text)
    for i in range(len(url_name_li)):
        url_id1, url_id2,= url_name_li[i]
        # 详情链接
        info_url = f'https://k.autohome.com.cn/detail/{url_id1}.html#pvareaid={url_id2}'
        res1 = requests.get(url=info_url, headers=header).text
        # print(res1)
        pl = re.findall(r'<p class="kb-item-msg">(.*?)<.p>', res1)
        print(pl)
        # print(type(pl))
        # print(pinpai2)
        # print(pinpai)
        new_list.append([pinpai,pl])
        print("*" * 100)
        print('爬取的评论个数：', i+1)
        time.sleep(1)
    return new_list

def run():
    # 翻页获取数据
    all_list = []
    all_list.append(["品牌", '评论'])
    # 爬取10页
    df=pd.read_csv('test3.csv')
    pinpai_list=df['0']
    id_list=df['2']
    for i in range(len(df)):
        pinpai=pinpai_list[i]
        id=id_list[i]
        print("当前爬取品牌：", pinpai, id)
        for page in range(1,500):
            data_text = get_data(id, page)
            print("*" * 100)
            if '<p>暂无口碑数据</p>'in data_text:
                print('当前产品爬取完毕')

                break
            print("当前爬取品牌：", pinpai)
            print('爬取评论页数：', page)
            out_date = data_deal(pinpai, data_text)
            all_list += out_date
            data_to_csv(all_list)
            time.sleep(2)
if __name__ == '__main__':
    run()