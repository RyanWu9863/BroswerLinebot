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
    if re.match('推薦景點',user_message):
        carousel_template_message = TemplateSendMessage(
            alt_text='熱門旅行景點',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/Ay7IkdS.jpg',
                        title='台北',
                        text='Taipei',
                        actions=[
                            MessageAction(
                                label='導覽',
                                text='台北是一座熱鬧的大都會，在這裡，亮麗的摩天大樓和香煙裊裊的古廟彼此共存。 您可以前往台北 101 眺望市景，然後再前往西門町盡情購物 (當然，一定要手拿一杯珍珠奶茶)。 晚上的時候，您可以踏遍眾多夜市品嚐美食。 這裡有超大雞排到臭豆腐等街頭美食，絕對會讓您上癮，等不及要吃下更多美食。'
                            ),
                            URIAction(
                                label='詳細資訊',
                                uri='https://www.tripadvisor.com.tw/Tourism-g293913-Taipei-Vacations.html'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/7NRdD4E.jpg',
                        title='台中',
                        text='Taichung',
                        actions=[
                            MessageAction(
                                label='導覽',
                                text='在眾多的旅遊景點中，台中有類似於東京或曼哈頓的熱鬧購物體驗、繁華的夜生活，還有各式各樣的美食，就算是最挑剔的老饕，也能盡興而歸。 來到這座城市，旅客可以在寺廟、市場、公園和博物館大飽眼福。 如果是全家出遊，不妨前往台中國立自然科學博物館，或前往逢甲夜市購買本地商品。 不過，台中最有名的是泡沫紅茶，這可以說是台中最有名的飲料。'
                            ),
                            URIAction(
                                label='詳細資訊',
                                uri='https://www.tripadvisor.com.tw/Tourism-g297910-Taichung-Vacations.html'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/l32E20S.jpg',
                        title='台南',
                        text='Tainan',
                        actions=[
                            MessageAction(
                                label='導覽',
                                text='臺南為臺灣最具歷史的都市，過去曾為臺灣首府，目前則是兼具商業氣息與歷史人文的現代都市。 臺南也是宗教信仰的中心，擁有上千所寺院其中並包括全台首學孔子廟，且慶典、遶境盛會不絕。 漫步國華街，一路品嘗臺灣特產與閒逛在地傳統菜場和市集。 參觀臺灣歷史博物館，一探臺灣人物與歷史。 奇美博物館坐擁美麗花園，蒐羅藝術品和樂器等私人收藏。'
                            ),
                            URIAction(
                                label='詳細資訊',
                                uri='https://www.tripadvisor.com.tw/Tourism-g293912-Tainan-Vacations.html'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, carousel_template_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=user_message))
        
    if user_message == "電影推薦":
        image_carousel_template_message = TemplateSendMessage(
            alt_text='電影推薦清單',
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
                    ]
                )
            )
        line_bot_api.reply_message(
            reply_token=event.reply_token,
            messages=[image_carousel_template_message]
        )    


#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
