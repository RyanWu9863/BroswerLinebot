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
from flask import Flask, request, jsonify
import requests
import feedparser
app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('S7DP6ph0sWeOWVyIr9c7ZV3NuqYkVlTfY5+CSnWblopXBqRFYuU8HSaaAQ9nNWYo3Ufdm/q6OxemxpP7wqFw5XwXkFvlwaf+pwKdp5BlgewaeaVILO3FUi5xbISRjNyhSzMGxIfVEn6HWYVeOiyzqQdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('65be4975efb12e6e52a9ef33e73f393b')

line_bot_api.push_message('U99de7fa38147448fa75424b52482549f', TextSendMessage(text='你可以開始了'))

# # 監聽所有來自 /callback 的 Post Request
# @app.route("/callback", methods=['POST'])
# def callback():
#     # get X-Line-Signature header value
#     signature = request.headers['X-Line-Signature']

#     # get request body as text
#     body = request.get_data(as_text=True)
#     app.logger.info("Request body: " + body)

#     # handle webhook body
#     try:
#         handler.handle(body, signature)
#     except InvalidSignatureError:
#         abort(400)

#     return 'OK'

@handler.add(MessageEvent, message=TextMessage)

# LINE Webhook Endpoint
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    user_message = data['events'][0]['message']['text']

    # 天氣查詢
    if user_message.startswith("天氣"):
        location = user_message.split(" ")[1]
        weather_info = get_taiwan_weather(location)
        return reply_message(weather_info)
    
    # 新聞查詢
    elif user_message.startswith("新聞"):
        category = user_message.split(" ")[1]
        news_info = fetch_taiwan_news(category)
        return reply_message(news_info)
    
    # 未識別的訊息
    else:
        return reply_message("請輸入有效指令，例如：天氣 台北 或 新聞 財經")

# 回應格式
def reply_message(text):
    return jsonify({
        "replyToken": "xxx",
        "messages": [{"type": "text", "text": text}]
    })

def get_taiwan_weather(location):
    api_key = "CWA-3995D289-1BE9-45B6-AD6F-5496915DB347"
    url = f"https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={api_key}&locationName={location}"
    response = requests.get(url).json()
    try:
        location_data = response['records']['location'][0]
        weather = location_data['weatherElement'][0]['time'][0]['parameter']['parameterName']
        temperature = location_data['weatherElement'][2]['time'][0]['parameter']['parameterName']
        return f"{location} 天氣：{weather}，溫度：{temperature}°C"
    except IndexError:
        return "查無此地區天氣資訊，請確認地名是否正確。"

def fetch_taiwan_news(category):
    # 定義 RSS 來源
    rss_sources = {
        "最新": "https://news.ltn.com.tw/rss/focus.xml",
        "焦點": "https://news.ltn.com.tw/rss/politics.xml",
        "旅遊": "https://news.ltn.com.tw/rss/travel.xml",
        "政治": "https://news.ltn.com.tw/rss/politics.xml",
        "財經": "https://news.ltn.com.tw/rss/business.xml"
    }
    
    # 找不到分類的處理
    if category not in rss_sources:
        return "無法辨識分類，請選擇：最新、焦點、旅遊、政治、財經。"
    
    # 解析 RSS
    rss_url = rss_sources[category]
    feed = feedparser.parse(rss_url)
    news_list = []
    for entry in feed['entries'][:5]:
        news_list.append(f"{entry['title']} - {entry['link']}")
    return "\n".join(news_list)


#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)