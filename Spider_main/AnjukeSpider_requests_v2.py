import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
import time
import json


# 代理ip线程池api
def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


def get_html(url):
    retry_count = 5  # 容错次数
    proxy = get_proxy().get("proxy")  # 获取代理ip
    print(proxy)
    while retry_count > 0:
        try:
            html = requests.get(url, proxies={"http": "http://{}".format(proxy)})
            # 使用代理访问
            return html
        except Exception:
            retry_count -= 1
    # 出错5次, 删除代理池中代理
    delete_proxy(proxy)
    return None  # 如果请求失败则返回None


# 爬虫api
def start_requests(url):
    USER_AGENT = ua.random
    print(USER_AGENT)
    headers = {
        "User-Agent": USER_AGENT,
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8"}
    rep = requests.get(url, headers=headers)
    return rep.content


def parse(content, old_url):
    soup = BeautifulSoup(content, 'html.parser')
    link_list = soup.find_all("a", attrs={"class": "houseListTitle"})

    for link in link_list:
        my_dict = {}
        my_dict['title'] = link['title']
        my_dict['href'] = link['href']
        result_list.append(my_dict)
    next_page = soup.find('a', class_='aNxt')
    if next_page:
        time.sleep(3)
        next_url = next_page['href']
        text = start_requests(next_url)
        parse(text, next_url)
        write_json(result_list)
    else:
        print("防爬机制已阻拦，需要人工操作")
        driver = webdriver.Chrome()
        driver.get(old_url)
        driver.maximize_window()


def write_json(result):
    s = json.dumps(result, indent=4, ensure_ascii=False)
    with open('links.json', 'w', encoding='utf-8') as f:
        f.write(s)


if __name__ == '__main__':
    ua = UserAgent()
    result_list = []
    base_url = "https://beijing.anjuke.com/sale/p1-v3/#filtersort"
    try:
        # base_text = start_requests(base_url)
        base_text = get_html(base_url)
        parse(base_text, base_url)
        # write_json(result_list)
    except Exception:
        pass
    finally:
        write_json(result_list)


