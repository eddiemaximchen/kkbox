import requests
import pymysql
import json
import ast
#資料庫連線
def createHTML():
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
                #TAB
        str='<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">'
        str=str+'<link href="css\\tab.css" rel="stylesheet"><link href="css\\style.css" rel="stylesheet" type="text/css">'
        str=str+'<script src="scripts\\tab.js"></script>'  
        str=str+'</head><header>KKBOX Demo</header><body onload="document.getElementById(\'defaultOpen\').click();">'
        str=str+'<div class="activity"><button class="tablinks" onclick="openAct(event, \'board\')" id="defaultOpen">榜單</button>'
        str=str+'<button class="tablinks" onclick="openAct(event, \'chart\')" id="showChart">歌單</button>'
        str=str+'<button class="tablinks" onclick="openAct(event, \'rank\')">排行榜</button>'
        str=str+'<button class="tablinks" onclick="openAct(event, \'playtab\')">播放清單</button></div>'
        str=str+'<div id="board" class="tabcontent">'
                # 榜單
        with conn.cursor() as cursor:
            command="select id,title,img_url from boards"
            cursor.execute(command)
        result = cursor.fetchall()
        str=str+'<select id="selectBoard" onchange="showData(\'home\');">'
        str=str+'<option value="" selected>請選擇榜單</option>'
        for item in result:
            str=str+'<option value="%s'%item["id"]+'">'+item["title"]+'</option>'
        str=str+'</select><br><img src="./images/logo.png">'
        #當前分類有多少歌
        str=str+'</div><div id="chart" class="tabcontent"><h3 id="song_num"></h3><img src="./images/prev.png" onclick="showData(\'prev\')")"><img src="./images/home.png" onclick="showData(\'home\')"><img src="./images/next.png" onclick="showData(\'next\')">'
                        # 按鈕 
        str=str+'<div class="add"><table id="btn">'
        with conn.cursor() as cursor:
            command="select boards.id,boards.title as title, song_name, song_url from charts join boards on charts.board_id=boards.id order by charts.board_id"
            cursor.execute(command)
            cursor.close
        result = cursor.fetchall()          
        for item in result:       
            str=str+'<tr class="'+item["id"]+'"><td><button onclick="window.open(\'https://www.youtube.com/results?search_query=%s'%item['song_name']+'\')">播放MV</button></td><td><button  onclick="playlist(\'add\',\'%s'%item['song_name']+'\')">加入播放清單</button></td></tr>'               
                        # 歌單
        str=str+'</table></div><table id="song_list">'#不能加<div>否則playlist無法運作
        for item in result:     #song_name格式不符 寫不進去格式要改UTF-8
            str=str+'<tr class="'+item["id"]+'"><td>%s'%item["title"]+'</td><td id="%s'%item["song_name"]+'"><a href="%s'%item["song_url"]+'">%s'%item["song_name"]+'</td></tr>'
        str=str+'</table></div>'#不能刪</div>否則playlist無法運作
        str=str+'<div id="rank" class="tabcontent">'
                # 排行榜
        with conn.cursor() as cursor:
            command="select count(*) as counts, charts.song_name as name from charts join hits on hits.song_url=charts.song_url group by charts.song_name order by count(*) desc limit 10"
            cursor.execute(command)
            cursor.close
        result = cursor.fetchall()
        for item in result:
            str=str+'<button onclick="playsong(\'%s'%item['name']+'\')">播放歌曲</button>'+item['name']+'--點擊次數---%d'%item['counts']+'<br>'
        str=str+'</div>'
                #播放清單
        str=str+'<div id="playtab" class="tabcontent"><table id="playlist"></table></div>'
        str=str+'<footer>陳信佑期中報告</footer></body></html>'

        fileobj =open('index.html', 'wt',encoding='UTF-8')
        print(str,file=fileobj)
        fileobj.close()
if __name__=="__main__":  
        createHTML()
