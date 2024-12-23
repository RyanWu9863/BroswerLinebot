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

@handler.add(MessageEvent, message=TextMessage)

# LINE Webhook Endpoint
def handle_message(event):
    user_message = event.message.text

    if user_message.startswith("天氣"):
        location = user_message.split(" ")[1] if len(user_message.split(" ")) > 1 else "台北"
        weather_info = get_taiwan_weather(location)
        reply_text = weather_info
    elif user_message.startswith("新聞"):
        category = user_message.split(" ")[1] if len(user_message.split(" ")) > 1 else "最新"
        news_info = fetch_taiwan_news(category)
        reply_text = news_info
    else:
        reply_text = "請輸入有效指令，例如：天氣 台北 或 新聞 財經"

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

def get_taiwan_weather(location):
    api_key = "CWA-3995D289-1BE9-45B6-AD6F-5496915DB347"
    url = f"https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={api_key}&locationName={location}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        location_data = data['records']['location'][0]
        weather = location_data['weatherElement'][0]['time'][0]['parameter']['parameterName']
        temperature = location_data['weatherElement'][2]['time'][0]['parameter']['parameterName']
        return f"{location} 天氣：{weather}，溫度：{temperature}°C"
    except requests.exceptions.RequestException:
        return "無法取得天氣資訊，請稍後再試。"
    except IndexError:
        return "查無此地區天氣資訊，請確認地名是否正確。"

def fetch_taiwan_news(category):
    rss_sources = {
        "最新": "https://news.ltn.com.tw/rss/focus.xml",
        "焦點": "https://news.ltn.com.tw/rss/politics.xml",
        "旅遊": "https://news.ltn.com.tw/rss/travel.xml",
        "政治": "https://news.ltn.com.tw/rss/politics.xml",
        "財經": "https://news.ltn.com.tw/rss/business.xml"
    }
    if category not in rss_sources:
        return "無法辨識分類，請選擇：最新、焦點、旅遊、政治、財經。"

    rss_url = rss_sources[category]
    try:
        feed = feedparser.parse(rss_url)
        if not feed.entries:
            return "無法取得新聞，請稍後再試。"
        return "\n".join(f"{entry['title']} - {entry['link']}" for entry in feed.entries[:5])
    except Exception:
        return "無法取得新聞資訊，請稍後再試。"


#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)