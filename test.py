# -*- coding: utf-8 -*-

#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re
app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('S7DP6ph0sWeOWVyIr9c7ZV3NuqYkVlTfY5+CSnWblopXBqRFYuU8HSaaAQ9nNWYo3Ufdm/q6OxemxpP7wqFw5XwXkFvlwaf+pwKdp5BlgewaeaVILO3FUi5xbISRjNyhSzMGxIfVEn6HWYVeOiyzqQdB04t89/1O/w1cDnyilFU=')

# 必須放上自己的Channel Secret
handler = WebhookHandler('65be4975efb12e6e52a9ef33e73f393b')

line_bot_api.push_message('U99de7fa38147448fa75424b52482549f', TextSendMessage(text='你可以開始了'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message =event.message.text
    if re.match('我想出去玩',user_message):
        carousel_template_message = TemplateSendMessage(
            alt_text='熱門旅行景點',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/Ay7IkdS.jpg',
                        title='北部推薦景點',
                        text='North',
                        actions=[
                            MessageAction(
                                label='導覽',
                                text='台灣北部擁有多元景點，如懷舊山城九份老街、自然美景陽明山、奇特地質野柳、夕陽迷人的淡水老街、傳統文化平溪天燈，以及台北101與士林夜市的現代繁華。'
                            ),
                            URIAction(
                                label='詳細資訊',
                                uri='https://taiwantour.net/taiwan-attractions/'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/7NRdD4E.jpg',
                        title='中部推薦景點',
                        text='West',
                        actions=[
                            MessageAction(
                                label='導覽',
                                text='台灣中部有清境農場的高山美景、日月潭的湖光山色、鹿港小鎮的古樸風情，以及谷關溫泉的休閒享受，融合自然與人文魅力。'
                            ),
                            URIAction(
                                label='詳細資訊',
                                uri='https://travel.line.me/article/A1fp6dm8v0'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/l32E20S.jpg',
                        title='南部推薦景點',
                        text='South',
                        actions=[
                            MessageAction(
                                label='導覽',
                                text='台灣南部有墾丁的熱帶沙灘、佛光山的宗教文化、高雄港的繁華夜景，以及台南古城的歷史遺跡，展現多元風貌。'
                            ),
                            URIAction(
                                label='詳細資訊',
                                uri='https://yoke918.tw/tag/%E5%8D%97%E9%83%A8%E6%97%85%E9%81%8A%E6%99%AF%E9%BB%9E/'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/616EwoZ.jpg',
                        title='東部推薦景點',
                        text='East',
                        actions=[
                            MessageAction(
                                label='導覽',
                                text='台灣東部擁有太魯閣壯麗峽谷、清水斷崖海岸美景、花蓮七星潭的碧海藍天，以及台東鹿野高台的熱氣球嘉年華，魅力十足。'
                            ),
                            URIAction(
                                label='詳細資訊',
                                uri='https://fullfen.tw/taitung-lazy-bag/'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, carousel_template_message)
        
    elif re.match('我想看電影',user_message):
        image_carousel_template_message = TemplateSendMessage(
            alt_text='推薦電影清單',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/miOnNkN.jpg',
                        action=PostbackAction(
                            label='SPY×FAMILY',
                            display_text=(
                                "劇情介紹: 劇場版《SPY×FAMILY CODE: White》由作者遠藤達哉監製，描述佛傑一家北國旅遊的溫馨故事。"
                                "上映日期: 2024/1/19\n觀看預告片: https://www.youtube.com/watch?v=-4g5k-WoT-g"
                            ),
                        data='action=SPY_FAMILY'
                            )
                        ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/UKtun5m.jpg',
                        action=PostbackAction(
                            label='排球少年',
                            display_text=(
                                "劇情介紹: 烏野高中與音駒高中的宿命對決，精彩排球大賽即將展開！"
                                "上映日期: 2024/4/12\n觀看預告片: https://www.youtube.com/watch?v=gK6RbuM3U7Y"
                            ),
                                data='action=HAIKYUU'
                            )
                        ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/v49IxTk.jpg',
                        action=PostbackAction(
                            label='小丑：雙重瘋狂',
                            display_text=(
                                "劇情介紹: 小丑亞瑟在精神病院中遇見哈莉·奎茵，展開危險又扭曲的愛情故事。"
                                "上映日期: 2024/10/2\n觀看預告片: https://www.youtube.com/watch?v=rIhJSOArJVc"
                            ),
                                data='action=JOKER'
                            )
                        ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/47cHVwl.jpg',
                        action=PostbackAction(
                            label='夏天隧道，再見出口',
                            display_text=(
                                "劇情介紹: 一場跨越時間與空間的奇幻冒險，探索隧道的奧秘。"
                                "上映日期: 2022/12/2\n觀看預告片: https://www.youtube.com/watch?v=Izh-45jS3DE"
                            ),
                                data='action=SUMMER_TUNNEL'
                            )
                        )
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/stm5m9e.jpg',
                        action=PostbackAction(
                            label='更多電影',
                            display_text=(
                                "更多電影介紹:http://www.atmovies.com.tw/movie/next/"                              
                            ),
                                data='action=SUMMER_TUNNEL'
                            )
                        )
                    ]
                )
            )
        line_bot_api.reply_message(event.reply_token, image_carousel_template_message)
        
    elif re.match('我想吃飯',user_message):
        carousel_template_message = TemplateSendMessage(
            alt_text='推薦餐廳',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/LGjze2M.jpg',
                        title='北部推薦美食',
                        text='North',
                        actions=[
                            MessageAction(
                                label='介紹',
                                text='台北永康街的小籠包、士林夜市雞排，基隆廟口的蚵仔煎，淡水老街的阿給，還有新竹城隍廟的米粉與貢丸湯，地方特色讓人回味無窮！'
                            ),
                            URIAction(
                                label='詳細資訊',
                                uri='https://www.welcometw.com/%E5%8F%B0%E5%8C%97%E7%BE%8E%E9%A3%9F%E6%8E%A8%E8%96%A6/'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/MmtibnZ.jpg',
                        title='中部推薦美食',
                        text='West',
                        actions=[
                            MessageAction(
                                label='導覽',
                                text='中部美食獨具魅力，彰化肉圓彈牙香濃，南投日月潭阿薩姆紅茶濃郁，台中太陽餅與逢甲夜市美食應有盡有，苗栗客家小炒與擂茶更是風味十足，讓人一試成主顧！'
                            ),
                            URIAction(
                                label='詳細資訊',
                                uri='https://www.welcometw.com/%e5%8f%b0%e4%b8%ad%e7%be%8e%e9%a3%9f%e9%a4%90%e5%bb%b3%e6%8e%a8%e8%96%a6%ef%bd%9c%e7%b2%be%e9%81%b8-12-%e9%96%93%e5%8f%b0%e4%b8%ad%e5%bf%85%e5%90%83%e7%be%8e%e9%a3%9f%e3%80%8a%e9%8d%8b%e7%89%a9/'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/HnHzZDr.jpg',
                        title='南部推薦美食',
                        text='South',
                        actions=[
                            MessageAction(
                                label='導覽',
                                text='南部美食充滿熱情，台南的牛肉湯與虱目魚粥鮮美，旗津的海產與烤小卷超讚，鹽埕的蚵仔煎與冬瓜茶經典，還有墾丁的炸鮮奶與大街小吃，絕對令人難忘！'
                            ),
                            URIAction(
                                label='詳細資訊',
                                uri='https://www.welcometw.com/%e5%8f%b0%e5%8d%97%e7%be%8e%e9%a3%9f/'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/c5YLRbi.jpg',
                        title='東部推薦美食',
                        text='East',
                        actions=[
                            MessageAction(
                                label='導覽',
                                text='東部美食天然純樸，花蓮的炸彈蔥油餅與扁食鮮美，台東池上的米飯香Q，長濱的海鮮新鮮可口，還有阿美族的烤山豬肉與小米麻糬，濃濃原民風味令人難忘！'
                            ),
                            URIAction(
                                label='詳細資訊',
                                uri='https://www.welcometw.com/%E5%8F%B0%E6%9D%B1%E7%BE%8E%E9%A3%9F%E6%8E%A8%E8%96%A6/'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, carousel_template_message)        
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='請輸入「我想出去玩」、「我想看電影」或「我想吃飯」'))

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
