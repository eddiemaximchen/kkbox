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

    db_settings = {
        "host": "1ocalhost",
        "port": 3306,
        "user": "root",
        "password": "123456",
        "db": "kkbox",
        "charset": "utf8"
    }
    conn = pymysql.connect(host='localhost',
                        user='root',
                        password='123456',
                        database='kkbox',
                        charset='utf8',
                        cursorclass=pymysql.cursors.DictCursor
                        )

        # 建立Cursor物件
    with conn.cursor() as cursor:
        # 新增資料SQL語法
        command = "INSERT INTO boards(id, title)VALUES(%s, %s)"

        for item in result:
            cursor.execute(command, (item["id"],item["title"]))     #TypeError: 'NoneType' object is not iterable      
                
        # 儲存變更
        conn.commit()
if __name__=="__main__":
        get_charts()

# 資料庫參數設定
