from DBUtils import DBUtils
import datetime

db = DBUtils()
link_title = '\"DROP TABLE anjuke_3d\"'
link_href = "https://beijing.anjuke.com/prop/view/A1960798140?from=esf_list_spfy&spread=filtersearch&invalid=1&click_url=https://lego-click.anjuke.com/jump?target=pZwY0ZnlsztdraOWUvYKuaYzmHEvmH7-riYdryw6sHEzPjTVrH-BPiY3PAD3nARBryEkuH0KnHTkrjTOnWTvTEDQnWbLPjnknjcznHTznjcYTHDOPjTkTHDOPjTkTHD_nHnKnHTkTHDdrjDkPWD1PHEkPHEKnE7AEzdEEzdKibfb8C1hBmfhBs4MoufG9cM-BFxCCpWGCUNKnEDQTEDVnEDKnHczPHmLPjm3nW0kn191rHc1n9DvTgK60h7V01NknHCzTHDKuycduj0vm1cVnvw-niYYPycksHbkmycVujDYPyubrj9YnAPbTHDznWNvP1Evrjc3nWbvPW91PHcKnHczPHmLPjm3nW0vPW01P1EkrTDKTEDKTiYKTE7CIZwk01CfsvF-pyGGUh08myOJIyV-shPfUiq1myQ-sLm1skDLEYnLEYEQniYLEW-DsNwDrj0VEWDvPaYdrj-7PbNYPjnLPWcKnWcQsWE8nWDksWDLn9DkTHTKTHD_nHnKXLYKnHTkn1NKnHTknHmYrT7BPHuBPHF6uid-uANksHEzuHcVmW9znaYznvwBnHR-uAnzPWnKTHEKTED1THDknakQnjnksjm3PWmKuAR-Pj9znyn1mHDQrH0dn9&uniqid=pc5e3d14eab5e471.57504653&position=1&kwtype=filter&now_time=1581061354"
link_3d = "https://www.anjuke.com/pc/esf/vrview/?token=lpWqx52S5%2FVjwI%2BIdbayZvV4QZ8DOWBANWbyjGHT9BOSi7O%2FWZr0HmRrG1Ar2F0A&app_id=10002&city_id=14&from=propview&from=prop_view"
dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
sql = 'INSERT IGNORE INTO anjuke_3d_copy (name, web_site, 3d_link, create_time)' \
                          'VALUES("%s","%s","%s","%s")' % \
                          (str(link_title), str(link_href), str(link_3d), dt)

db.operate_data(sql)
db.commit_data()
db.close()
