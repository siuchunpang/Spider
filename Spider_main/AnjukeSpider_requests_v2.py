# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from DBUtils import DBUtils
import requests
import time
import datetime
import random

ua = UserAgent()
db = DBUtils()
spider_count = 1


# 代理ip线程池
def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


# 爬虫相关
def get_html(url):
    USER_AGENT = ua.random
    headers = {
        "User-Agent": USER_AGENT,
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8"}

    retry_count = 5  # 容错次数
    proxy = get_proxy().get("proxy")  # 获取代理ip
    print("开始第%d次爬虫" % spider_count)
    print("代理ip为：" + str(proxy))
    print("User-agent：" + USER_AGENT)
    while retry_count > 0:
        try:
            resp = requests.get(url, headers=headers, proxies={"http": "http://{}".format(proxy)})
            resp.encoding = 'utf-8'
            html = resp.text
            return html
        except Exception:
            retry_count -= 1
    # 出错5次, 删除代理池中代理
    delete_proxy(proxy)
    return None  # 如果请求失败则返回None


def parse(content):
    global spider_count
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    soup = BeautifulSoup(content, 'html.parser')
    link_list = soup.find_all("a", attrs={"class": "houseListTitle"})
    print("开始解析...")

    for link in link_list:
        sql = 'INSERT IGNORE INTO anjuke_3d (name, web_site, create_time)' \
          'VALUES("%s","%s","%s")' % \
          (str(link['title']), str(link['href']), dt)
        db.operate_data(sql)
        db.commit_data()

    print("解析完成！")
    next_page = soup.find('a', class_='aNxt')
    if next_page:
        spider_count += 1
        time.sleep(random.random() * 6)
        next_url = next_page['href']
        next_url_text = get_html(next_url)
        parse(next_url_text)
    else:
        if spider_count == 50:
            print("爬取完毕")
        else:
            print("防爬机制已阻拦，需要人工操作")
            driver = webdriver.Chrome()
            driver.get("https://beijing.anjuke.com/sale/v3/")
            driver.maximize_window()
            time.sleep(8)


if __name__ == '__main__':
    base_url = "https://beijing.anjuke.com/sale/v3/"
    try:
        base_text = get_html(base_url)
        parse(base_text)
    except Exception as e:
        print(e)
    finally:
        db.close()
        print(spider_count)
