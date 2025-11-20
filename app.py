from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)

# 首頁路由
@app.route('/')
def index():
    return render_template('index.html')

# 搜尋路由 (目前先回傳假資料，之後會串 scraper.py)
@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    artist = data.get("artist")
    media = data.get("media")
    date_range = data.get("dateRange")

    # TODO: 這裡之後會改成真實爬蟲結果
    sample_results = [
        {
            "title": f"【假新聞】{artist} 出席活動",
            "media": "ETtoday",
            "link": "https://www.ettoday.net/",
            "date": datetime.now().strftime("%Y-%m-%d"),
        },
        {
            "title": f"【假新聞】{artist} 受訪談近況",
            "media": "自由時報",
            "link": "https://ent.ltn.com.tw/",
            "date": datetime.now().strftime("%Y-%m-%d"),
        }
    ]

    return jsonify(sample_results)

if __name__ == '__main__':
    # 設定 port 與 debug 模式
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
