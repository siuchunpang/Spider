import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import random
import json

ua = UserAgent()
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
            html = requests.get(url, headers=headers, proxies={"http": "http://{}".format(proxy)})
            # 使用代理访问
            return html.content
        except Exception:
            retry_count -= 1
    # 出错5次, 删除代理池中代理
    delete_proxy(proxy)
    return None  # 如果请求失败则返回None


def parse(content):
    global spider_count
    soup = BeautifulSoup(content, 'html.parser')
    link_list = soup.find_all("a", attrs={"class": "houseListTitle"})
    print("开始解析...")

    for link in link_list:
        my_dict = {}
        my_dict['title'] = link['title']
        my_dict['href'] = link['href']
        result_list.append(my_dict)

    print("解析完成！")
    next_page = soup.find('a', class_='aNxt')
    if next_page:
        spider_count += 1
        time.sleep(random.random()*3)
        next_url = next_page['href']
        next_url_text = get_html(next_url)
        parse(next_url_text)
    else:
        if spider_count == 50:
            print("爬取完毕")
        else:
            print("防爬机制已阻拦，需要人工操作")


def write_json(result):
    s = json.dumps(result, indent=4, ensure_ascii=False)
    with open('links.json', 'w', encoding='utf-8') as f:
        f.write(s)


if __name__ == '__main__':
    result_list = []
    base_url = "https://beijing.anjuke.com/sale/v3/"
    try:
        base_text = get_html(base_url)
        parse(base_text)
    except Exception:
        pass
    finally:
        write_json(result_list)
        print(spider_count)


