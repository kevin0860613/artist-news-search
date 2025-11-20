import requests
import os
from datetime import datetime

def search_news(artist, media_list, date_range, start_date=None, end_date=None):
    api_key = os.getenv("GNEWS_API_KEY")
    base_url = "https://gnews.io/api/v4/search"

    # 日期處理
    today = datetime.now().strftime("%Y-%m-%d")
    if date_range == "today":
        start_date = end_date = today
    elif date_range == "week":
        from datetime import timedelta
        monday = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime("%Y-%m-%d")
        start_date = monday
        end_date = today
    elif date_range == "month":
        start_date = f"{datetime.now().year}-{datetime.now().month:02d}-01"
        end_date = today

    params = {
        "q": artist if artist != "all" else " OR ".join(media_list),
        "lang": "zh",
        "country": "tw",
        "from": start_date,
        "to": end_date,
        "max": 20,
        "token": api_key
    }

    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        return [{"title": "⚠️ 錯誤", "media": "GNews API", "link": "#", "date": str(response.status_code)}]

    data = response.json()
    articles = data.get("articles", [])
    results = []
    for article in articles:
        results.append({
            "title": article["title"],
            "media": article["source"]["name"],
            "link": article["url"],
            "date": article["publishedAt"][:10]
        })
    return results
