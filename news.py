import requests

def get_news():
    api_key = "73f4a1974f104ae3b322e7e356ad6f9d"
    url = f"https://newsapi.org/v2/top-headlines?country=tw&apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        articles = data['articles'][:5]
        news_list = [f"{i+1}. {article['title']}" for i, article in enumerate(articles)]
        return "\n".join(news_list)
    else:
        return "無法取得新聞資訊，請稍後再試。"
