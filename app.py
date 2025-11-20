from flask import Flask, render_template, request
from datetime import datetime, timedelta, date
import requests
import urllib.parse
import calendar

app = Flask(__name__)

# 完整的藝人名單 (用於下拉選單)
ARTISTS = [
    "陳浩民", "林子聰", "苑瓊丹", "李蒨蓉", "林美貞", "林國基", "徐新洋", 
    "宋蕊安(Soa)", "劉怡里營養師", "王中皇", "蔣偉文", "段鈞豪", "李培禎", 
    "陳為民", "林義傑", "張振榕", "莘妮", "謝懷德", "檢 場", "謝麗金", 
    "林佳儀", "潘逸安", "Vivian", "張伯森", "潘明德", "曲艾玲", "艾力克斯", 
    "李詠嫻", "徐乃麟", "林嘉俐", "蔡逸帆", "余荃斌(No name)", "林凱文", 
    "潘若迪", "游書庭", "劉丞", "李翊君"
]

# 優先查詢的新聞媒體清單 (用於複選框)
MEDIA_SITES = {
    "聯合報": "udn.com",
    "中國時報": "chinatimes.com",
    "鏡新聞": "mnews.tw",
    "自由時報": "ltn.com.tw",
    "壹蘋新聞網": "tw.nextapple.com",
    "ETtoday": "ettoday.net",
    "三立新聞網": "setn.com",
    "Yahoo新聞": "tw.news.yahoo.com",
    "TVBS新聞網": "news.tvbs.com.tw",
    "CTWANT": "ctwant.com",
    "LIFE生活網": "life.tw",
    "Nownews": "nownews.com",
    "車勢新聞": "autos.udn.com", # 範例，需要更精確的官網
    "噓星聞": "stars.udn.com" # 範例，需要更精確的官網
}

# --- 輔助函式：計算日期範圍 ---
def calculate_date_range(time_period):
    """根據選擇計算當天、當周或當月的開始日期和結束日期"""
    today = date.today()
    
    if time_period == 'today':
        start_date = today
    elif time_period == 'this_week':
        # 該周一到該日
        start_date = today - timedelta(days=today.weekday())
    elif time_period == 'this_month':
        # 該月1號到該日
        start_date = date(today.year, today.month, 1)
    else: # 預設為全部時間
        return None, None
        
    return start_date, today

# --- 模擬/實際 API 搜尋函式 ---
def perform_complex_search(artist, selected_media, time_period):
    """
    根據使用者選擇，建構進階 Google 搜尋字串並模擬查詢。
    
    實際部署時，你需要將這裡的模擬邏輯替換為真實的 Google Custom Search API 呼叫，
    或是一個更專業的 API 服務。
    """
    
    # 1. 處理日期範圍
    start_date, end_date = calculate_date_range(time_period)
    
    # Google 搜尋中的日期範圍語法: after:YYYY-MM-DD before:YYYY-MM-DD
    date_query = ""
    if start_date and end_date:
        # Google 搜尋引擎不直接支援精確到日的 after/before 篩選，
        # 但許多新聞 API 支援。這裡使用一個近似的自訂參數或留白。
        # ⚠️ 注意: 真正的 Google 搜尋 API 不直接支援此精確日期篩選。
        date_query = f" (從 {start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')})"

    # 2. 建構媒體網站限制
    site_query = ""
    if selected_media:
        # site:udn.com OR site:chinatimes.com
        sites = [f"site:{MEDIA_SITES[m]}" for m in selected_media if m in MEDIA_SITES]
        if sites:
            site_query = " OR ".join(sites)
            site_query = f" ({site_query})"

    # 3. 組合完整的查詢字串
    # 目標: "藝人名" AND ("關鍵字" OR site:A OR site:B) (日期限制描述)
    full_query = f'"{artist}" 新聞 {site_query} {date_query}'
    
    # 這裡只返回模擬結果
    if artist == "陳浩民" and time_period == "this_month":
        return [
            f"[聯合報]{artist} 與妻慶祝結婚週年，感情甜蜜如初。",
            f"[鏡新聞]{artist} 談及新作挑戰，演技再獲肯定。",
            f"[其他新聞]陳浩民投資副業傳聞，經紀公司出面澄清。"
        ]
    
    # 4. 模擬回傳
    if site_query or date_query:
        return [
            f"搜尋藝人：{artist}",
            f"搜尋範圍：{'、'.join(selected_media) if selected_media else '全部媒體'}",
            f"時間範圍：{time_period} ({start_date.strftime('%Y/%m/%d')} ~ {end_date.strftime('%Y/%m/%d')})",
            "--- 模擬結果 ---",
            f"新聞標題範例：{artist} 近期活動引發網路熱議。",
            f"新聞標題範例：{artist} 澄清不實報導。",
        ]
    
    return [f"請選擇藝人，並嘗試不同篩選條件。"]


@app.route('/', methods=['GET', 'POST'])
def index():
    news_results = []
    selected_artist = ""
    selected_media = []
    time_period = "all"
    
    if request.method == 'POST':
        selected_artist = request.form.get('artist_select')
        time_period = request.form.get('time_period')
        # 獲取所有被勾選的媒體
        selected_media = request.form.getlist('media_check')

        if selected_artist:
            news_results = perform_complex_search(selected_artist, selected_media, time_period)

    return render_template('index.html', 
                           artists=ARTISTS, 
                           media_sites=MEDIA_SITES, 
                           news_results=news_results,
                           selected_artist=selected_artist,
                           selected_media=selected_media,
                           time_period=time_period)

if __name__ == '__main__':
    # 在本機運行 (開發模式)
    app.run(debug=True)
