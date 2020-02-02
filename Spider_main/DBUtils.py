# -*- coding: utf-8 -*-
import pymysql
import configparser
import datetime
import json
import warnings

warnings.filterwarnings('ignore')

# 读取配置文件
cf = configparser.ConfigParser()
cf.read('db.config')
host = cf.get('db', 'host')
port = cf.get('db', 'port')
port = int(port)
user = cf.get('db', 'user')
pwd = cf.get('db', 'passwd')
db = cf.get('db', 'db')
charset = cf.get('db', 'charset')


class DBUtils:
    def __init__(self):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
        self.port = port
        self.get_conn()

    # 获取数据库连接
    def get_conn(self):
        try:
            self.conn = pymysql.connect(host=host, port=port, user=user, passwd=pwd, db=db, charset=charset)
        except pymysql.Error as e:
            print("数据库连接失败：", e)
        finally:
            self.cursor = self.conn.cursor()

    # 选择数据
    def get_data_from_db(self, sql):
        try:
            self.cursor.execute(sql)
        except pymysql.Error as e:
            print('执行查询SQL失败,错误信息:', e)
        finally:
            return self.cursor.fetchall()

    # 提交数据
    def commit_data(self):
        try:
            self.conn.commit()
        except pymysql.Error as e:
            # print('Mysql Error %d: %s' % (e.args[0], e.args[1]))
            print(e)

    # 回滚数据
    def rollback_data(self):
        try:
            self.conn.rollback()
        except pymysql.Error as e:
            # print('Mysql Error %d: %s' % (e.args[0], e.args[1]))
            print(e)

    # 操作数据
    def operate_data(self, sql):
        try:
            self.cursor.execute(sql)
        except pymysql.Error as e:
            # 执行SQL失败，则回滚事务
            print('操作失败，回滚事务', e)
            self.rollback_data()

    # 关闭数据库连接
    def close(self):
        try:
            self.cursor.close()
            self.conn.close()
        except pymysql.Error as e:
            # print('Mysql Error %d: %s' % (e.args[0], e.args[1]))
            print(e)


if __name__ == '__main__':
    error_title = ''
    error_href = ''
    with open("links.json", "r", encoding="utf8") as f:
        datas = json.loads(f.read())

    db = DBUtils()
    title = "宾阳里 独立一居 可厅截2居 南北通透 阳光房 交通购物方便"
    href = "https://beijing.anjuke.com/prop/view/A1963474700?from=esf_list_spfy&spread=filtersearch&invalid=1&click_url=https://lego-click.anjuke.com/jump?target=pZwY0ZnlsztdraOWUvYKuadWP1DYrj6bnzYzPywhsHwWuycVmhnYridBPHN3ryEQuW01mHmKPj0LnjE3PkDKnHnknW0vPH0LnHmYPjbYnEDQP1nknTDQP1nknTDQsjD1THDknTDQPH9kPWnYnW9OrHmYTHDKwbnVNDnVENGsOsJnOChsOCB4OlvUlmaFOmBgl2AClpAdTHDKnEDKsHDKTHDznWn3rjTvrHnLnH0vrHmdnHcKP97kmgF6UgndnjDln9DQTyDzujIbPWb1sHmYPAmVPjFhnadBmyR-sH--nWT3rjIbujbvuEDQnWc1rj9kPWb1rH0LP1cvrH0vTHDznWn3rjTvrHnOnHTvn1EYrHmKTEDKTEDVTEDKpZwY0ZnlszqBuy-JpyOMsh78pMRouiOWUvYf0v7_uiqvnztKnH9kEHwDPHTVP1KKEBYOPH6AsHTYnbnVPYF7PYcdEWEOPDwKTHczni3YsWcQna3QP1cKnTDkTEDQsjD1TgVqTHDknjndTHDknjDvPj9KPAm3rAmdmyEVnHc1uiYYmh7WsH6WmvDVnyEduj0LP10vnhEzTEDYTEDKnkDQnjT_nHT1PzkvrHD1TynYnAFbrHPWP1TLnjKWuhN&uniqid=pc5e3690b2b7f704.98857820&position=1&kwtype=filter&now_time=1580634290"
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        for data in datas:
            error_title = data["title"]
            error_href = data["href"]
            sql = 'INSERT IGNORE INTO anjuke_3d_test (name, web_site, create_time)' \
              'VALUES("%s","%s","%s")' % \
              (data["title"], data["href"], dt)
            db.operate_data(sql)
            db.commit_data()
    except UnicodeDecodeError as e:
        print("title：", error_title)
        print("href：", error_href)
        print(e)
    finally:
        db.close()
