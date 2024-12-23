#載入LineBot所需要的套件
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from weather import get_weather
from news import get_news
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
def handle_message(event):
    user_message = event.message.text
    if "天氣" in user_message:
        response = get_weather()
    elif "新聞" in user_message:
        response = get_news()
    else:
        response = "請輸入「天氣」或「新聞」來獲取資訊。"
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response))

# def get_taiwan_weather(location):
#     api_key = "CWA-3995D289-1BE9-45B6-AD6F-5496915DB347"
#     url = f"https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={api_key}&locationName={location}"
#     try:
#         response = requests.get(url, timeout=10)
#         response.raise_for_status()
#         data = response.json()
#         location_data = data['records']['location'][0]
#         weather = location_data['weatherElement'][0]['time'][0]['parameter']['parameterName']
#         temperature = location_data['weatherElement'][2]['time'][0]['parameter']['parameterName']
#         return f"{location} 天氣：{weather}，溫度：{temperature}°C"
#     except requests.exceptions.RequestException:
#         return "無法取得天氣資訊，請稍後再試。"
#     except IndexError:
#         return "查無此地區天氣資訊，請確認地名是否正確。"

# # 必須放上自己的 NewsAPI API Key
# NEWS_API_KEY = "73f4a1974f104ae3b322e7e356ad6f9d"

# def fetch_taiwan_news(keyword):
#     url = f"https://newsapi.org/v2/top-headlines?country=tw&category={news_category}&apiKey={NEWS_API_KEY}"

#     try:
#         response = requests.get(url, timeout=10)
#         response.raise_for_status()
#         data = response.json()

#         if data["status"] != "ok" or not data["articles"]:
#             return "查無相關新聞，請嘗試其他關鍵字。"

#         # 組合新聞資訊
#         articles = data["articles"]
#         return "\n".join(f"{article['title']} - {article['url']}" for article in articles)
#     except requests.exceptions.RequestException:
#         return "無法取得新聞資訊，請稍後再試。"


#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)