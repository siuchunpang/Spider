from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import json


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    dr = webdriver.Chrome(options=chrome_options)
    return dr


def parse(driver, content):
    soup = BeautifulSoup(content, 'html.parser')
    link_list = soup.find_all("a", attrs={"class": "houseListTitle"})

    for link in link_list:
        my_dict = {}
        my_dict['title'] = link['title']
        my_dict['href'] = link['href']
        result_list.append(my_dict)
        has_next_page = driver.find_element_by_class_name("aNxt")
        if has_next_page:
            time.sleep(5)
            has_next_page.click()
            content = driver.page_source
            parse(driver, content)
        else:
            driver.close()


def write_json(result):
    s = json.dumps(result, indent=4, ensure_ascii=False)
    with open('links.json', 'w', encoding='utf-8') as f:
        f.write(s)


def main(url):
    driver = get_driver()
    driver.get(url)
    content = driver.page_source
    try:
        parse(driver, content)
    except NoSuchElementException as e:
        print(e)
    finally:
        driver.close()
        write_json(result_list)


if __name__ == '__main__':
    url = "https://beijing.anjuke.com/sale/v3/"
    result_list = []
    main(url)

