import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
import time
import json


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


def parse(content):
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
            parse(text)
            write_json(result_list)
        else:
            print("防爬机制已阻拦")
            next_url_bak = next_page['href']
            driver = webdriver.Chrome()
            driver.get(next_url_bak)
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
        base_text = start_requests(base_url)
        parse(base_text)
        # write_json(result_list)
    except TimeoutError:
        pass
    finally:
        write_json(result_list)


