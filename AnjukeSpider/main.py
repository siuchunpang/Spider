# -*- coding: utf-8 -*-
from Spider import Spider
from DBUtils import DBUtils

if __name__ == '__main__':
    spider = Spider()
    db = DBUtils()
    base_url = "https://beijing.anjuke.com/sale/v3/"
    try:
        base_text = spider.get_html(base_url)
        spider_count = spider.parse(base_text)
        print(spider_count)
    except Exception as e:
        print(e)
    finally:
        db.close()
