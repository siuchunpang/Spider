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
import sys
import os


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
    def get_html(self, url, encoding=0, spider_num=0):
        USER_AGENT = self.ua.random
        headers = {
            "User-Agent": USER_AGENT,
            "Connection": "keep-alive",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8"}

        retry_count = 5  # 容错次数
        proxy = self.get_proxy().get("proxy")  # 获取代理ip
        if spider_num == 1:
            print("第%d次爬虫" % self.spider_count)
            print("代理ip为：" + str(proxy))
            print("User-agent：" + USER_AGENT)
        while retry_count > 0:
            try:
                resp = requests.get(url, headers=headers, proxies={"http": "http://{}".format(proxy)})
                if encoding == 0:
                    resp.encoding = 'utf-8'
                    html = resp.text
                else:
                    html = resp.content
                return html
            except Exception:
                retry_count -= 1
        # 出错5次, 删除代理池中代理
        self.delete_proxy(proxy)
        return None  # 如果请求失败则返回None

    def parse_3d(self, text):
        soup = BeautifulSoup(text, 'html.parser')
        try:
            link_3d_div = soup.find('div', id='qj_pic_wrap')
            if link_3d_div is not None:
                link_3d_element = link_3d_div.div.iframe
                link_3d = link_3d_element["src"]
                return link_3d
            else:
                print("该房间没有3D场景")
                self.spider_error()
                return ""
        except Exception as e:
            print("parse_3d_error：", e)
            sys.exit()

    # 不录入数据库
    def parse(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        link_list = soup.find_all("a", attrs={"class": "houseListTitle"})

        if link_list is not None:

            print("开始解析网站...")

            for link in link_list:
                link_title = link['title']
                link_title = self.validate_title(link_title)
                link_href = link['href']

                # 爬取场景链接
                link_href_text = self.get_html(link_href)
                link_3d = self.parse_3d(link_href_text)

                # 在3D看房列表中有些房间没有3D场景
                if link_3d == "":
                    pass
                else:
                    # 爬取场景图片
                    link_img_text = self.get_html(link_3d, spider_num=1)
                    shoot_count = self.parse_img(link_img_text, link_title)

            print("解析网站完成！")
            next_page = soup.find('a', class_='aNxt')
            if next_page is not None:
                self.spider_count += 1
                time.sleep(random.random() * 6)
                next_url = next_page['href']
                next_url_text = self.get_html(next_url, 1)
                self.parse(next_url_text)
            else:
                if self.spider_count == 50:
                    print("爬取完毕")
                    return self.spider_count
                else:
                    self.spider_error()
        else:
            self.spider_error()

    # # 录入数据库
    # def parse(self, content):
    #     soup = BeautifulSoup(content, 'html.parser')
    #     link_list = soup.find_all("a", attrs={"class": "houseListTitle"})
    #
    #     if link_list is not None:
    #
    #         print("开始解析网站...")
    #
    #         for link in link_list:
    #             link_title = link['title']
    #             link_title = self.validate_title(link_title)
    #             link_href = link['href']
    #             dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #
    #             # 爬取场景链接
    #             link_href_text = self.get_html(link_href)
    #             link_3d = self.parse_3d(link_href_text)
    #
    #             # 在3D看房列表中有些房间没有3D场景
    #             if link_3d == "":
    #                 sql = 'INSERT IGNORE INTO anjuke (name, web_site, 3d_link, create_time, shoot_count)' \
    #                       'VALUES("%s","%s","%s","%s","%d")' % (str(link_title), str(link_href), str(link_3d), dt, 0)
    #             else:
    #                 # 爬取场景图片
    #                 link_img_text = self.get_html(link_3d, spider_num=1)
    #                 shoot_count = self.parse_img(link_img_text, link_title)
    #                 sql = 'INSERT IGNORE INTO anjuke (name, web_site, 3d_link, create_time, shoot_count)' \
    #                       'VALUES("%s","%s","%s","%s","%d")' % \
    #                       (str(link_title), str(link_href), str(link_3d), dt, int(shoot_count))
    #             self.db.operate_data(sql)
    #             self.db.commit_data()
    #
    #         print("解析网站完成！")
    #         next_page = soup.find('a', class_='aNxt')
    #         if next_page is not None:
    #             self.spider_count += 1
    #             time.sleep(random.random() * 6)
    #             next_url = next_page['href']
    #             next_url_text = self.get_html(next_url, 1)
    #             self.parse(next_url_text)
    #         else:
    #             if self.spider_count == 50:
    #                 print("爬取完毕")
    #                 return self.spider_count
    #             else:
    #                 self.spider_error()
    #     else:
    #         self.spider_error()

    def parse_img(self, text, scene_name):
        # time.sleep(random.random() * 3)
        scene_path = "F:\\AutoTest\\Spider\\AnjukeSpider\\"
        data_3d_list = re.findall(r'VRHOUSE_DATA_3D = (.+?)    </script>', text)
        if not data_3d_list:
            data_3d_list = re.findall(r'\(\'vrdataload\',(.+?)\);', text)
        if data_3d_list is not []:
            if not os.path.exists(scene_path + "scene\\%s" % scene_name):
                print('创建文件夹:%s' % scene_name)
                os.mkdir(scene_path + "scene\\%s" % scene_name)

            print("开始解析图片%d..." % self.img_count)
            self.img_count += 1

            try:
                data_3d = data_3d_list[0].replace("\\", "")
                data = json.loads(data_3d, strict=False)
                hotspots = data['HotSpots']

                for hotspots_index, hotspot in enumerate(hotspots):
                    img_links = hotspot['TileImagesPath']

                    if not os.path.exists(scene_path + "scene\\%s\\hotspot_%s" % (scene_name, hotspots_index)):
                        # print('创建文件夹:hotspot_%s' % hotspots_index)
                        os.mkdir(scene_path + "scene\\%s\\hotspot_%s" % (scene_name, hotspots_index))

                    for img_links_index, img_link in enumerate(img_links):
                        img_link_name = img_link[24:56]
                        # print("图片名称:%s_%d.jpg" % (img_link_name, img_links_index))
                        html = self.get_html(img_link, encoding=1)
                        with open(scene_path + "\\scene\\%s\\hotspot_%s\\%s_%d.jpg" % (scene_name, hotspots_index, img_link_name, img_links_index),
                                  'wb') as file:
                            file.write(html)

                print("解析图片完成！")
                shoot_count = len(hotspots)
                return shoot_count
            except Exception as e:
                self.db.close()
                print("parse_img_error：", e)

        else:
            self.spider_error()

    def spider_error(self):
        self.db.close()
        print("防爬机制已阻拦，需要人工操作")
        driver = webdriver.Chrome()
        driver.get("https://beijing.anjuke.com/sale/v3/")
        driver.maximize_window()
        time.sleep(8)
        return self.spider_count

    def validate_title(self, title):
        rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        new_title = re.sub(rstr, "_", title)  # 替换为下划线
        return new_title
