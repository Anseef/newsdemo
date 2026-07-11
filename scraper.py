import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# ==========================================
# 1. CONFIGURATION & CONFIG CONSTANTS
# ==========================================
# Google News RSS URL targeted at South Indian Education (Past 7 Days)
RSS_URL = "https://news.google.com/rss/search?q=(KEAM+OR+TNEA+OR+EAMCET+OR+COMEDK+OR+KCET)+education+when:7d&hl=en-IN&gl=IN&ceid=IN:en"

# Path where your frontend reads the news data
JSON_FILE_PATH = "src/data/NewsData.json"


# ==========================================
# 2. SCRAPING ENGINE
# ==========================================
def fetch_latest_news():
    """
    Fetches the latest South Indian educational news from Google News RSS.
    """
    print("1. Contacting Google News RSS...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(RSS_URL, headers=headers, timeout=10)
        print(f"2. Google responded with Status Code: {response.status_code}")
    except Exception as e:
        print(f"❌ Failed to reach Google News: {e}")
        return []
    
    soup = BeautifulSoup(response.content, features="html.parser")
    items = soup.findAll('item')
    print(f"3. Found {len(items)} total articles in the RSS feed.")
    
    new_articles = []
    
    # Process the top 10 most recent headlines
    for idx, item in enumerate(items[:10]):
        title_text = item.title.text.split(" - ")[0].strip()
        link_text = item.link.text.strip()
        pub_date = datetime.now().strftime("%Y-%m-%d")
        
        print(f"   -> Scraping: {title_text[:50]}...")
        
        # Dynamic State & Course matching based on keywords
        state = "South India"
        courses = ["B.Tech", "B.E"]
        if any(kw in title_text for kw in ["KEAM", "LBS", "Kerala"]):
            state = "Kerala"
            courses = ["B.Tech", "B.Pharm"]
        elif any(kw in title_text for kw in ["TNEA", "Tamil Nadu", "Anna Univ"]):
            state = "Tamil Nadu"
        elif any(kw in title_text for kw in ["EAMCET", "EAPCET", "AP ", "TS ", "Telangana", "Andhra"]):
            state = "Telangana & AP"
            courses = ["B.Tech", "B.Pharm", "B.Sc Agriculture"]
        elif any(kw in title_text for kw in ["COMEDK", "KCET", "Karnataka", "KEA"]):
            state = "Karnataka"

        # Dynamic Tag and UI Colors based on headline keywords
        tag = "News Update"
        color = "#1B6CA8"  # Default Blue
        bg = "#EBF5FF"
        icon = "🎓"
        
        lower_title = title_text.lower()
        if any(kw in lower_title for kw in ["allotment", "result", "rank", "merit"]):
            tag = "Allotment Live"
            color = "#059669"  # Emerald Green
            bg = "#ECFDF5"
            icon = "🎯"
        elif any(kw in lower_title for kw in ["counselling", "option", "choice", "registration"]):
            tag = "Counselling"
            color = "#7C3AED"  # Purple
            bg = "#F5F0FF"
            icon = "🖥️"
        elif any(kw in lower_title for kw in ["date", "extended", "deadline", "last day", "postponed"]):
            tag = "Urgent Alert"
            color = "#DC2626"  # Red
            bg = "#FFF0F0"
            icon = "🚨"

        article_obj = {
            "id": int(datetime.now().strftime("%y%m%d%H%M")) + idx,
            "icon": icon,
            "color": color,
            "bg": bg,
            "tag": tag,
            "title": title_text[:90],
            "date": "Recent Update",
            "publishedAt": pub_date,
            "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=400&q=80",
            "description": f"Official announcement regarding {title_text}. Students are advised to log into the official examination portal to verify their admission status, review cutoff schedules, and complete required procedures.",
            "eligibility": "Qualified entrance exam candidates with valid Plus Two / Intermediate academic records.",
            "applyLink": link_text,
            "courses": courses,
            "state": state
        }
        new_articles.append(article_obj)
        
    return new_articles


# ==========================================
# 3. DEDUPLICATION & STORAGE ENGINE
# ==========================================
def append_to_json_file(new_articles, file_path=JSON_FILE_PATH):
    """
    Appends new articles while preventing duplicates.
    Inserts newest items at index 0.
    """
    existing_data = []
    
    # Ensure the directory exists (e.g., creates 'src/data' if missing)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # 1. Read existing data safely
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                existing_data = json.load(file)
                if not isinstance(existing_data, list):
                    existing_data = []
        except json.JSONDecodeError:
            print(f"⚠️ Warning: '{file_path}' was empty or corrupted. Starting fresh.")
            existing_data = []
    else:
        print(f"ℹ️ Creating new data file at '{file_path}'...")

    # 2. Extract existing titles (lowercased) to detect duplicates
    existing_titles = {item.get("title", "").lower().strip() for item in existing_data}
    
    # 3. Filter and append only unique articles
    added_count = 0
    for article in new_articles:
        clean_title = article["title"].lower().strip()
        if clean_title not in existing_titles:
            # Insert at top of list so newest updates appear first in your React UI
            existing_data.insert(0, article)
            existing_titles.add(clean_title)
            added_count += 1
        else:
            print(f"   [Skipped] Already saved: {article['title'][:40]}...")

    # 4. Write updated list back to disk
    if added_count > 0:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(existing_data, file, indent=2, ensure_ascii=False)
        print(f"\n✅ Success! Added {added_count} new articles to '{file_path}'. Total saved: {len(existing_data)}")
    else:
        print(f"\nℹ️ No new unique articles found today. '{file_path}' remains unchanged.")


# ==========================================
# 4. MAIN EXECUTION ENTRY POINT
# ==========================================
if __name__ == "__main__":
    print("--- Starting Vidyabhyasam News Scraper ---")
    scraped_news = fetch_latest_news()
    if scraped_news:
        append_to_json_file(scraped_news, file_path=JSON_FILE_PATH)
    else:
        print("❌ No news fetched. Exiting script.")
    print("--- Scraping Session Finished ---")