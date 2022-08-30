import os
from datetime import datetime
import random
from flask import Flask, abort, request

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage

app = Flask(__name__)

Dino_Random =[
  'Dino是五股張震🧑‍🦼','Dino好帥','每天都被自己帥醒','Dino是藍天大師'
]

Alex4_Random =[
  '四~爺~~~~💕','四爺豪棒棒👍','四爺何時要請客','四爺最常約ㄆㄠˇ惹～','四爺要找喵喵嗎？'
]

StockMsg_Random=[
  '買啊～哪次不買',
  '我全都要～',
  '多買一些分給大家啊🎁',
  '我賣身也買不起～',
  '歐印啦!還想什麼~',
  '問就是買,歐印!'
]

Fxx_Random=[
  '幫你補個幹~',
  '乾~~~',
  '金派耶~',
  '好兇喔',
  '深呼吸喘口氣',
  '你再說一次看看...'
]

# 越前面優先權越高
SearchKey1 = '抽抽'
SearchKey2 = 'qq'
SearchKey3 = '四爺'
SearchKey4 = 'QQ'
SearchKey5 = 'D哥'
SearchKey6 = '吃啥'
SearchKey7 = '乾'
SearchKey8 = '買'
SearchKey9 = '抽籤'
SearchKey10 = '運勢'
SearchKey11 = '吃什麼'

# 記得要一起改
String_Search_Key=[
  SearchKey1,SearchKey2,SearchKey3,SearchKey4,SearchKey5,SearchKey6,SearchKey7,SearchKey8,SearchKey9,SearchKey10,SearchKey11
]

Reply_Message = {
  SearchKey1:'randomIMG',
  SearchKey2:'幫你擦眼淚',
  SearchKey3:random.choices(Alex4_Random)[0],
  SearchKey4:'別哭了,需要衛生紙嗎',
  SearchKey5: random.choices(Dino_Random)[0],
  SearchKey6:'RandomK6',
  SearchKey7:random.choices(Fxx_Random)[0],
  SearchKey8:random.choices(StockMsg_Random)[0],
  SearchKey9:'求籤',
  SearchKey10:'求籤',
  SearchKey11:'RandomK6'#吃啥專用key
}

RandomK6 =[
  '我不知道~',
  '小芬你說呢?',
  '四爺要吃嗎?',
  '王董吃鍋嗎?',
  '猜拳決定啦',
  '那你想吃什麼',
  '吃土惹～～',
  '吃雞！',
  '三寶~'
  '吃鍋',
  '吃紅',
  '我要吃涮乃葉',
  '我要吃肉多多',
  '看你們吃我就很開心惹~',
  '>>吃香蕉<<',
  '喝奶就飽惹~~',
  '吃水餃',
  '吃樹下',
  '吃火車便當',
  '吃便當',
  '吃泰式料理'
]

# 隨機圖片用
Random_img =[
  'https://cdn.clickme.net/gallery/fb0ff9d6499cb30ea015c72cee75fe50.jpg',
  'https://cdn.clickme.net/gallery/c74b770910e58636dacdaa74e52e0626.jpg',
  #'http://5b0988e595225.cdn.sohucs.com/images/20200324/99af72909ec54cde89cb63465be3f40d.jpeg',
  #'http://i0.hdslb.com/bfs/archive/f0af9ae0eae29c1f57fa641612ba9f8d00dda431.jpg',
  'https://i1.wp.com/i1.hdslb.com/bfs/archive/5ce343f3646f062b958638544e365f40ae71ca1f.jpg',
  #'https://www.taisounds.com/ucms/uPages/img.aspx?FileLocation=%2FPJ-TAISOUNDS%2FFiles%2F&FileName=photo-12622-t.JPG',
  'https://cdn.discordapp.com/attachments/955826448311128084/957247698464043068/2022-03-26_7.31.49.png',
  'https://i.imgur.com/1kXU4if.jpg',
  #貓貓圖
  #奇怪的知識
  'https://memeprod.sgp1.digitaloceanspaces.com/user-wtf/1604995167673.jpg',
  'http://i2.kknews.cc/WE7x0Nb6XChVFx8fxkUpuo8IKGiMwt0/0.jpg' # 如花 
]

#抽籤用
fortune = ['大吉','中吉', '吉', '末吉', '小凶', '凶', '大凶']
prob = [8, 11, 30, 15, 10, 5, 2]

# 處理message用
def process_textstring(msg,):
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
  elif get_reply_msg == 'RandomK6':
    keyresult = random.choice(RandomK6)
    return ['text',keyresult]
  elif get_reply_msg == '求籤':
    keyresult = random.choices(fortune, weights=prob)[0]
    #return ['text',f'Hi~{profilename}\n占卜的結果為\n\n\n===>> {keyresult} <<===']
    return ['text',f'|||--占卜的結果為--|||\n\n\n===>> {keyresult} <<===']
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
        #UserId = event.source.user_id
        #profile = line_bot_api.get_profile(UserId)
        #checkMsg = process_textstring(event.message.text, profile.display_name)
        checkMsg = process_textstring(event.message.text)
        if checkMsg[0] == 'text' :
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=checkMsg[1]))
        elif checkMsg[0] == 'img' :
            line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url=checkMsg[1],preview_image_url=checkMsg[1]))


