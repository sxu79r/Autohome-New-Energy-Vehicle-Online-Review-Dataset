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
    df.to_csv(f"数据集07.csv", index=False)
def data_deal(id,pinpai,data_text):
    '''数据解析'''
    pos_list = []
    neg_list = []
    sum = 0 #记录总爬取评论
    # 详情链接+车名
    url_name_li = re.findall(r'href="https://k.autohome.com.cn/detail/(.*?).html#pvareaid=(\d+)" rel="noreferrer">查看完整口碑<i class="list_arrow_right__EtpQA list_icon__aL4pn"><.i><.a>', data_text)
    for i in range(len(url_name_li)):
        url_id1, url_id2,= url_name_li[i]
        # 详情链接
        info_url = f'https://k.autohome.com.cn/detail/{url_id1}.html#pvareaid={url_id2}'
        res1 = requests.get(url=info_url, headers=header).text
        # print(res1)
        pos_pl_2 = re.findall(r'                <h1>最满意<.h1>\n                <p class="kb-item-msg">(.*?)<.p>', res1)
        pos_pl_1 = re.findall(r'                <h1>新车好评<.h1>\n                <p class="kb-item-msg">(.*?)<.p>', res1)
        neg_pl_1 = re.findall(r'                <h1>最不满意<.h1>\n                <p class="kb-item-msg">(.*?)<.p>', res1)
        neg_pl_2 = re.findall(r'                <h1>新车槽点<.h1>\n                <p class="kb-item-msg">(.*?)<.p>', res1)
        # print(pos_pl_2,'|', pos_pl_1,'|', neg_pl_2,'|', neg_pl_1)
        # print(type(pl))
        # print(pinpai2)
        # print(pinpai)
        if len(pos_pl_2) != 0:
            pos_list.append([pinpai, id, pos_pl_2[:], 1])
        if len(pos_pl_1) != 0:
            pos_list.append([pinpai, id, pos_pl_1[:], 1])
        if len(neg_pl_2) != 0:
            neg_list.append([pinpai, id, neg_pl_2[:], 0])
        if len(neg_pl_1) != 0:
            neg_list.append([pinpai, id, neg_pl_1[:], 0])
        # print(neg_list, pos_list)
        print("*" * 100)
        print('爬取的评论个数：', i+1)
        sum += 1
        time.sleep(0.5)
    return pos_list, neg_list, sum

def run():
    # 翻页获取数据
    sum = 0 #记录爬取数量
    n_list = 0 #记录数据集数量
    all_list = []
    all_list.append(["品牌",'id','评论', 'label'])
    # 爬取10页
    df=pd.read_csv('数据集网址07.csv')
    pinpai_list=df['0']
    id_list=df['2']
    for i in range(len(df)):
        if int(sum/9000)==n_list+1:
            all_list = []
            all_list.append(["品牌",'id', '评论', 'label'])
        pinpai=pinpai_list[i]
        id=id_list[i]
        print("当前爬取品牌：", pinpai, id)
        for page in range(1,500):
            data_text = get_data(id, page)
            print("*" * 100)
            if '<p>暂无口碑数据</p>'in data_text:
                print('当前产品爬取完毕')
                break
            print("当前爬取品牌：", pinpai, id)
            print('爬取评论页数：', page)
            pos_data,neg_data,temp = data_deal(id,pinpai, data_text)
            sum+=temp
            # 每爬取9000条评论就退出，因为代码会重启导致前面的重爬
            if sum >9000:
                return
            print(sum)
            if len(pos_data)!=0:
                all_list += pos_data
            if len(neg_data) != 0:
                all_list += neg_data
            data_to_csv(all_list)
            time.sleep(2)
if __name__ == '__main__':
    run()