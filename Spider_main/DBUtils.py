import pymysql
import configparser
import datetime
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
            print('Mysql Error %d: %s' % (e.args[0], e.args[1]))

    # 回滚数据
    def rollback_data(self):
        try:
            self.conn.rollback()
        except pymysql.Error as e:
            print('Mysql Error %d: %s' % (e.args[0], e.args[1]))

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
            print('Mysql Error %d: %s' % (e.args[0], e.args[1]))


if __name__ == '__main__':
    db = DBUtils()
    address = "https://beijing.anjuke.com/prop/view/A1935712970?from=esf_list_spfy&spread=filtersearch&invalid=1&click_url=https://lego-click.anjuke.com/jump?target=pZwY0ZnlsztdraOWUvYKuadbrjDvnHcLraYdnvNvsHwBnjTVrj0YnidhmW-BPAnYm1P-nhDKnHTkrHD3rjE1TEDQnWNkPHEQrHb3rHc1P10LTHDOnjTkTHDOnjTkTHD_nHnKnHTkTHDdrjTdn1bLnWE1nW0Kn97AEzdEEzdKibfb8C1hBmfhBs4MoufG9cM-BFxCCpWGCUNKnEDQTEDVnEDKnHczn1EOnHTzP1mYPWNvnWnkPTDvTgK60h7V01NknHCzTHDKPj9kPHc3Pj9VnynOuaYYnjNOsycYmvmVm19On19znyDLm19dTHDznWnYrHDknW0On1DLrHD1PWTKnHczn1EOnHTzP19Ln1TdPj0znTDKTEDKTiYKTE7CIZwk01CfsvF-pyGGUh08myOJIyV-shPfUiq1myQ-sLm1skD3wW9knNFjEBYdnYwjsHw7EbmVEH67raYkPjDYEYPAEbDOEYNKnWcQsWE8nWDksWDLn9DkTHTKTHD_nHnKXLYKnHTkn1NKnHTknHmYrTD3mvuBPhDdPiYLPWwbsHE1nyEVryELmzdhuyPWrH6bmHczuHnKTHEKTED1THDknakQPW9YsjcdPHmzTH9OPjKhrjnkuWu-PhEzPyc&uniqid=pc5e351f4cb9bfe6.03295951&position=2&kwtype=filter&now_time=1580539724"
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = 'INSERT IGNORE INTO anjuke_3d (name, web_site, create_time)' \
          'VALUES("%s","%s","%s")' % \
          ("华发蔚蓝堡", address, dt)
    db.operate_data(sql)
    db.commit_data()
    db.close()
