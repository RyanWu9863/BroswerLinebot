import requests

def get_weather(location):
    api_key = "49fb0eb9d77aca183081160dd1f71e47"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&lang=zh_tw&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_desc = data['weather'][0]['description']
        temp = data['main']['temp']
        return f"{location} 現在的天氣是 {weather_desc}，溫度 {temp}°C。"
    else:
        return "無法取得天氣資訊，請稍後再試。"
