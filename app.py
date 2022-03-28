import os
from datetime import datetime

from flask import Flask, abort, request

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage

app = Flask(__name__)

# 越前面優先權越高
SearchKey1 = '抽抽'
SearchKey2 = 'qq'
SearchKey3 = 'CC'
SearchKey4 = 'QQ'
SearchKey5 = 'D哥'
SearchKey6 = '吃啥'
SearchKey7 = '乾'

# 記得要一起改
String_Search_Key=[
  SearchKey1,SearchKey2,SearchKey3,SearchKey4,SearchKey5,SearchKey6,SearchKey7
]

Reply_Message = {
  SearchKey1:'randomIMG',
  SearchKey2:'幫你擦眼淚',
  SearchKey3:'幫你CC',
  SearchKey4:'別哭了,需要衛生紙嗎',
  SearchKey5:'D哥是藍天大師',
  SearchKey6:'你說呢',
  SearchKey7:'金派耶~'
}
                
# 隨機圖片用
Random_img =[
  'https://www.taisounds.com/ucms/uPages/img.aspx?FileLocation=%2FPJ-TAISOUNDS%2FFiles%2F&FileName=photo-12622-t.JPG',
  'https://cdn.discordapp.com/attachments/955826448311128084/957247698464043068/2022-03-26_7.31.49.png',
  #幹話王
  'https://i.imgur.com/1kXU4if.jpg'
  #貓貓圖
]

# 處理message用
def process_textstring(msg):
  keyresult = 'False'
  #預設找不到keyword, 若有則會把keyword記錄下來
  #在收到的msg中尋找是否有符合keyword
  for skey in range(len(String_Search_Key)):
    findkeyresult=msg.find(String_Search_Key[skey])
    if findkeyresult >= 0 :
      keyresult = String_Search_Key[skey]
      print(keyresult)
      break
      #找到後離開loop

  get_reply_msg=Reply_Message.get(keyresult,"False")
#  print(get_reply_msg) #印出keyword
  #檢查keyword
  if get_reply_msg.startswith('randomIMG'):  
    #隨機圖片
    img_Link= random.choice(Random_img)
    return ['img',img_Link]
  elif get_reply_msg == 'False':    
    #什麼都找不到
    return ['False',get_reply_msg]
  else: 
    #文字對應
    return ['text',Reply_Message.get(keyresult)]




line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))


@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return "Hello Heroku"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
        checkMsg = process_textstring(event.message.text)
        if checkMsg[0] == 'text' :
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=checkMsg[1]))
        elif checkMsg[0] == 'img' :
            line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url=checkMsg[1],preview_image_url=checkMsg[1]))


