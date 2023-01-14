var page=0;
function openAct(evt, ActName) {    //控制tab
    // Declare all variables
    var i, tabcontent, tablinks,imgcontent;
  
    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    } 

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
  
    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(ActName).style.display = "block";
    evt.currentTarget.className += " active";
    if (document.getElementById('selectBoard').value==""){
      document.getElementById('song_num').innerText="共有2677首歌" 
    }
  }
function showData(Act){        //控制歌單
    //跳到歌單

  document.getElementById('showChart').click();
  
  var selectBoard=document.getElementById('selectBoard'); 
  // Get all songs and buttons tr
  var boards = document.getElementById('song_list').getElementsByTagName("tr");
  var buttons= document.getElementById('btn').getElementsByTagName("tr"); 
  //Get selected board
  var board = selectBoard.value;
  //show songs from selected board
  //分頁 共2677首歌
  var count=0;
  
  if (Act=='prev'){
    page=page-1;
  }

  if (Act=='next'){
    page=page+1;
  }

  if (Act=='home'){
    page=0;
  }
  //for 之前要全部隱藏 for只管誰要顯示
  for (let i=0;i<boards.length;i++){
    boards[i].style.display = "none";
  }
  for (let i=0;i<buttons.length;i++){
    buttons[i].style.display = "none";
  }

  for (let i = 0; i <boards.length; i++) {
    if(board==""){
      count=count+1;
      if(count<page*20) {
        continue;
      }

      if( count>page*20 && count<(page*20)+20){
      	boards[count].style.display = "block";
      	buttons[count].style.display="block";
      }
    }
    else{
      if(boards[i].className ==board) {
        count=count+1;
        if(count<page*20) {
          continue;
        }

        if(count>page*20 && count<(page*20)+20){
          boards[count].style.display = "block";
          buttons[count].style.display= "block";
        }
      }
    }
  }
  var total_page=(count/20)
  if(count%20!=0){
    total_page=parseInt(total_page)+1;
  }
  document.getElementById('song_num').innerText="共有"+count+"首歌  第 "+(page+1)+" / "+total_page+"頁";  
  if((page+1)>total_page){
    showData('home');
  }
  if((page+1)==0){
    showData('home')
  }
}
function playlist(Act, song_name){    //控制播放清單
  var song=document.getElementById(song_name); // 該歌的TD
  var txt="";
  if (Act=="add"){
      txt=song.parentNode.innerHTML; //該歌的HTML
      var playlist=document.getElementById("playlist").innerHTML; // playlist table的HTML
      if(playlist.indexOf(song_name)==-1){  //表示該歌還沒出現在playlist上
          //把該歌加到playlist上 而且 tr的 id 等於歌名+1 因為歌名出現在很多地方
          txt="<tr id='"+song_name+"1'>"+txt+"<td><button onclick=\"playlist(\'del\',\'"+song_name+"\')\">移除</button></td></tr>";            
          playlist=playlist+txt;
          document.getElementById("playlist").innerHTML=playlist;
      }
  }
  else if (Act=="del"){
      song=document.getElementById(song_name+"1"); //找出playlist
      song.innerHTML="";//第一筆成功 後面都沒反應
  }
}
function playsong(song_name){
  var song=document.getElementById(song_name);
  var song_html=String(song.parentNode.lastChild.innerHTML);
  var url_start=song_html.indexOf('"');
  var url_end=song_html.lastIndexOf('"');
  var song_url=song_html.substring(url_start+1,url_end);
  window.open(song_url);
 
}
