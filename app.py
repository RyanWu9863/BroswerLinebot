# -*- coding: utf-8 -*-

# 載入 LineBot 所需要的套件
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import re
import os  # 確保匯入 os 模組

app = Flask(__name__)

# 必須放上自己的 Channel Access Token
line_bot_api = LineBotApi('66YmqXw11hVa6I7CBtb3gtWoTvhnhbXul0z6sX71D/5XQhOALiLzoDvo3wz7i0+15IXcV/LNdzLcBesfJN+71QSk8CFUfc8GnsZ9wmxdwxJ+jdNtNs7vneYrzoin9AfJ3gv6djQU5Hu9B7/g04bTRgdB04t89/1O/w1cDnyilFU=S7DP6ph0sWeOWVyIr9c7ZV3NuqYkVlTfY5+CSnWblopXBqRFYuU8HSaaAQ9nNWYo3Ufdm/q6OxemxpP7wqFw5XwXkFvlwaf+pwKdp5BlgewaeaVILO3FUi5xbISRjNyhSzMGxIfVEn6HWYVeOiyzqQdB04t89/1O/w1cDnyilFU=')

# 必須放上自己的 Channel Secret
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

# 訊息傳遞區塊
##### 基本上程式編輯都在這個 function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text

    # 功能：旅遊景點推薦
    if re.match('我想出去玩', user_message):
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
                                text='台灣北部擁有多元景點，如九份、陽明山、淡水等。'
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
                                text='台灣中部有清境農場、日月潭等迷人景點。'
                            ),
                            URIAction(
                                label='詳細資訊',
                                uri='https://travel.line.me/article/A1fp6dm8v0'
                            )
                        ]
                    )
                    # 可繼續加入其他地區的推薦
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, carousel_template_message)

    # 功能：電影推薦
    elif re.match('推薦電影', user_message):
        image_carousel_template_message = TemplateSendMessage(
            alt_text='推薦電影清單',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/miOnNkN.jpg',
                        action=PostbackAction(
                            label='SPY×FAMILY',
                            display_text=(
                                "劇情介紹: 北國旅遊溫馨故事。\n"
                                "上映日期: 2024/1/19\n"
                                "觀看預告片: https://www.youtube.com/watch?v=-4g5k-WoT-g"
                            ),
                            data='action=SPY_FAMILY'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/UKtun5m.jpg',
                        action=PostbackAction(
                            label='排球少年',
                            display_text=(
                                "劇情介紹: 烏野高中與音駒高中的宿命對決。\n"
                                "上映日期: 2024/4/12\n"
                                "觀看預告片: https://www.youtube.com/watch?v=gK6RbuM3U7Y"
                            ),
                            data='action=HAIKYUU'
                        )
                    )
                    # 可繼續加入其他電影推薦
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, image_carousel_template_message)

    # 功能：告訴我秘密（圖片訊息）
    elif re.match('告訴我秘密', user_message):
        image_message = ImageSendMessage(
            original_content_url='https://www.campus-studio.com/download/flag.jpg',
            preview_image_url='https://www.campus-studio.com/download/101.jpg'
        )
        line_bot_api.reply_message(event.reply_token, image_message)

    # 功能：附近的各樣式餐廳（Imagemap 訊息）
    elif re.match('附近的各樣式餐廳', user_message):
        imagemap_message = ImagemapSendMessage(
            base_url='https://i.imgur.com/ZLFh4RV.png',
            alt_text='推薦餐廳',
            base_size=BaseSize(height=1040, width=1040),
            actions=[
                URIImagemapAction(
                    link_uri='https://www.google.com/maps?q=日式料理',
                    area=ImagemapArea(x=0, y=0, width=520, height=520)
                ),
                URIImagemapAction(
                    link_uri='https://www.google.com/maps?q=西式料理',
                    area=ImagemapArea(x=520, y=0, width=520, height=520)
                ),
                URIImagemapAction(
                    link_uri='https://www.google.com/maps?q=中式料理',
                    area=ImagemapArea(x=0, y=520, width=520, height=520)
                ),
                 URIImagemapAction(
                    link_uri='https://www.google.com/maps?q=法式料理',
                    area=ImagemapArea(x=520, y=520, width=520, height=520)
                 )
                # 可繼續加入其他類型料理
            ]
        )
        line_bot_api.reply_message(event.reply_token, imagemap_message)

    # 預設回應
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=user_message))


# 主程式
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
