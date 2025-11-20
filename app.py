from flask import Flask, render_template, request, jsonify
from scraper import search_news
from datetime import datetime
import os

app = Flask(__name__)

# 首頁（顯示搜尋頁面）
@app.route('/')
def index():
    return render_template('index.html')

# 搜尋 API
@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        artist = data.get("artist")
        media = data.get("media", [])
        date_range = data.get("dateRange")
        start_date = data.get("startDate")
        end_date = data.get("endDate")

        # 呼叫 scraper.py 的真實新聞搜尋函式
        results = search_news(
            artist=artist,
            media_list=media,
            date_range=date_range,
            start_date=start_date,
            end_date=end_date
        )

        return jsonify(results)

    except Exception as e:
        return jsonify([{
            "title": "⚠️ 搜尋發生錯誤",
            "media": "系統",
            "link": "#",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "error": str(e)
        }])

# 啟動 Flask
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)


if __name__ == '__main__':
    # 設定 port 與 debug 模式
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
