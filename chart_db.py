import requests
import pymysql
import json
import ast
# 取得Token


def get_access_token():
    # API網址
    url = "https://account.kkbox.com/oauth2/token"

    # 標頭
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "account.kkbox.com"
    }
    # 參數
    data = {
        "grant_type": "client_credentials",
        "client_id": "60c2b618cc5a5da40311ee57845439a1",
        "client_secret": "5ff541909fa969da50e78a1421ec4b67"
    }
    access_token = requests.post(url, headers=headers, data=data)
    return access_token.json()["access_token"]
# 取得各種音樂排行榜列表

# 取得該音樂排行榜的歌曲列表
def get_charts_tracks(chart_id):
    #存取憑證
    access_token = get_access_token() 
    #取得音樂排行榜列表中的歌曲API網址
    url = "https://api.kkbox.com/v1.1/charts/" + chart_id + "/tracks"
    #標頭
    headers = {
        "accept": "application/json",
        "authorization": "Bearer " + access_token
    }
    #參數
    params = {
        "territory": "TW"  #台灣領域
    }
    response = requests.get(url, headers=headers, params=params)
    result = response.json()["data"]                            # class 'list' 
    # for item in result:                                         #若把result改成response 也會變NoneType
    #     print([item["name"], item["url"]])

    # 資料庫參數設定
    db_settings = {
        "host": "1ocalhost",
        "port": 3306,
        "user": "root",
        "password": "Tt-143085",
        "db": "kkbox",
        "charset": "utf8"
    }
    conn = pymysql.connect(host='localhost',
                        user='root',
                        password='Tt-143085',
                        database='kkbox',
                        charset='utf8',
                        cursorclass=pymysql.cursors.DictCursor
                        )

        # 建立Cursor物件
    with conn.cursor() as cursor:
        # 新增資料SQL語法
        command = "INSERT INTO charts(board_id,song_name, song_url)VALUES(%s,%s, %s)"

        for item in result:
            cursor.execute(command, (chart_id,item["name"], item["url"]))     #TypeError: 'NoneType' object is not iterable
            # 儲存變更
        conn.commit()

def get_charts():
    #取得存取憑證
    access_token = get_access_token() 
   #取得音樂排行榜列表API網址
    url = "https://api.kkbox.com/v1.1/charts"
    #標頭
    headers = {
        "accept": "application/json",
        "authorization": "Bearer " + access_token  #帶著存取憑證
    }
    #參數
    params = {
        "territory": "TW"  #台灣領域  
    }
    response = requests.get(url, headers=headers, params=params)
    result = response.json()["data"]                                
    for item in result:                                            
        get_charts_tracks(item["id"])
get_charts()