# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from DBUtils import DBUtils
import requests
import time
import datetime
import random
import json
import re


class Spider:
    def __init__(self):
        self.ua = UserAgent()
        self.db = DBUtils()
        self.spider_count = 1
        self.img_count = 1

    # 代理ip线程池
    def get_proxy(self):
        return requests.get("http://127.0.0.1:5010/get/").json()

    def delete_proxy(self, proxy):
        requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

    # 爬虫相关
    def get_html(self, url, id=0):
        USER_AGENT = self.ua.random
        headers = {
            "User-Agent": USER_AGENT,
            "Connection": "keep-alive",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8"}

        retry_count = 5  # 容错次数
        proxy = self.get_proxy().get("proxy")  # 获取代理ip
        if id == 0:
            print("开始第%d次爬虫" % self.spider_count)
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
        self.delete_proxy(proxy)
        return None  # 如果请求失败则返回None

    def parse_3d(self, text):
        soup = BeautifulSoup(text, 'html.parser')
        link_3d_soup = soup.find('div', id='qj_pic_wrap').div.iframe
        link_3d = link_3d_soup["src"]
        if link_3d_soup is not None:
            return link_3d
        else:
            self.spider_error()

    def parse(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        link_list = soup.find_all("a", attrs={"class": "houseListTitle"})

        if link_list is not None:

            print("开始解析网站...")

            for link in link_list:
                link_title = link['title']
                link_href = link['href']
                dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # 爬取场景链接
                link_href_text = self.get_html(link_href, 1)
                link_3d = self.parse_3d(link_href_text)

                # 爬取场景图片
                link_img_text = self.get_html(link_3d, 1)
                link_imgs = self.parse_img(link_img_text)

                sql = 'INSERT IGNORE INTO anjuke_3d_test (name, web_site, 3d_link, create_time, img_link1, img_link2, img_link3, img_link4, img_link5, img_link6)' \
                      'VALUES("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % \
                      (str(link_title), str(link_href), str(link_3d), dt, str(link_imgs[0]), str(link_imgs[1]), str(link_imgs[2]), str(link_imgs[3]), str(link_imgs[4]), str(link_imgs[5]))
                self.db.operate_data(sql)
                self.db.commit_data()

            print("解析网站完成！")
            next_page = soup.find('a', class_='aNxt')
            if next_page is not None:
                self.spider_count += 1
                time.sleep(random.random() * 6)
                next_url = next_page['href']
                next_url_text = self.get_html(next_url)
                self.parse(next_url_text)
            else:
                if self.spider_count == 50:
                    print("爬取完毕")
                    return self.spider_count
                else:
                    self.spider_error()
        else:
            self.spider_error()

    def parse_img(self, text):
        time.sleep(random.random() * 3)
        data_3d_list = re.findall(r'VRHOUSE_DATA_3D = (.+?)    </script>', text)
        if not data_3d_list:
            data_3d_list = re.findall(r'\(\'vrdataload\',(.+?)\)', text)
        if data_3d_list is not []:

            print("开始解析图片%d..." % self.img_count)
            self.img_count += 1

            try:
                data_3d = data_3d_list[0]
                data = json.loads(data_3d, strict=False)
                hotspots = data['HotSpots']
                hotspot = hotspots[0]
                img_links = hotspot['TileImagesPath']
                print("解析图片完成！")
                return img_links
            except Exception as e:
                print(e)

        else:
            self.spider_error()

    def spider_error(self):
        print("防爬机制已阻拦，需要人工操作")
        driver = webdriver.Chrome()
        driver.get("https://beijing.anjuke.com/sale/v3/")
        driver.maximize_window()
        time.sleep(8)
        return self.spider_count
