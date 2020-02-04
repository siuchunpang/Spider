# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests

ua = UserAgent()


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


def parse_3d(text):
    soup = BeautifulSoup(text, 'html.parser')
    link_3d_soup = soup.find('div', id='qj_pic_wrap').div.iframe
    link_3d = link_3d_soup["src"]
    if link_3d_soup:
        print(link_3d)
    else:
        print("防爬机制已阻拦，需要人工操作")
    # link_3d_soup = soup.find('div', id='qj_pic_wrap').children.children.iframe
    # link_3d = link_3d_soup['src']
    # print(link_3d)


if __name__ == '__main__':
    base_url = "https://beijing.anjuke.com/prop/view/A1912068142?from=esf_list_spfy&spread=filtersearch&click_url=https://lego-click.anjuke.com/jump?target=pZwY0ZnlsztdraOWUvYKuaYkuH9vPvDvPBYznvEksHEQPWNVmH6buaYdPjKWuH9QmHNdrANKP1c3PjnkP9DKnHczP10QnH0dP19dnWmLPTD1PWnknTD1PWnknTDQsjD1THDknTDQPH9kPWbOnW9QrHEzTHEKwbnVNDnVENGsOsJnOChsOCB4OlvUlmaFOmBgl2AClpAdTHDKnEDKsHDKTHDznWnYnWDYPjnvnH9OnHE1njEKP97kmgF6UgndnjDln9DQTHE1ujNLmyNzsH9OnHTVPAnkPaY3PhRbsy76PHE1nywWnyE3PTDQnWc1PjcQPjE1P1EkPHEOnHckTHDznWnYnWDYPjnvP1nYPjTzPHmKTEDKTEDVTEDKpZwY0ZnlszqBuy-JpyOMsh78pMRouiOWUvYf0v7_uiqvnztKPDujnH-KnbEVwbPaPaYLwNEdsNPKnHcVnNPjrDcdEbPAnDm1THczni3YsWcQna3QP1cKnTDkTEDQsjD1TgVqTHDknjndTHDknjDvPj9Kn1PWuAFhmyNVuWcdPiYYuWDQsyFbPjcVrHcQPjmzmHTzmHw-TEDYTEDKnkDQnjT_nHm3PakQnHNzPH9KmvczPvE1PhnznjnzrHczn9&uniqid=pc5e378e925bce60.81467468&position=4&kwtype=filter&now_time=1580699282"
    try:
        base_text = get_html(base_url)
        parse_3d(base_text)
    except Exception as e:
        print(e)
