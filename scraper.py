import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

# 1. Google News RSS URL targeted at South Indian Education (Last 24 Hours)s
RSS_URL = "https://news.google.com/rss/search?q=(KEAM+OR+TNEA+OR+EAMCET+OR+COMEDK+OR+KCET)+education+when:1d&hl=en-IN&gl=IN&ceid=IN:en"

def fetch_latest_news():
    print("Fetching live RSS feed...")
    response = requests.get(RSS_URL)
    soup = BeautifulSoup(response.content, features="xml")
    items = soup.findAll('item')
    
    new_articles = []
    
    for idx, item in enumerate(items[:4]):  # Grab top 4 daily headlines
        title_text = item.title.text.split(" - ")[0] # Remove news publisher name
        link_text = item.link.text
        pub_date = datetime.now().strftime("%Y-%m-%d")
        
        # Dynamic State & Course matching based on keywords
        state = "South India"
        courses = ["B.Tech", "B.E"]
        if "KEAM" in title_text or "LBS" in title_text or "Kerala" in title_text:
            state = "Kerala"
            courses = ["B.Tech", "B.Pharm"]
        elif "TNEA" in title_text or "Tamil Nadu" in title_text:
            state = "Tamil Nadu"
        elif "EAMCET" in title_text or "EAPCET" in title_text or "AP" in title_text or "TS" in title_text:
            state = "Telangana & AP"
            courses = ["B.Tech", "B.Pharm", "B.Sc Agriculture"]
        elif "COMEDK" in title_text or "KCET" in title_text or "Karnataka" in title_text:
            state = "Karnataka"

        # Dynamic Tag and UI Colors based on headline keywords
        tag = "News Update"
        color = "#1B6CA8" # Default Blue
        bg = "#EBF5FF"
        icon = "🎓"
        
        if "allotment" in title_text.lower() or "result" in title_text.lower():
            tag = "Allotment Live"
            color = "#059669" # Emerald Green
            bg = "#ECFDF5"
            icon = "🎯"
        elif "counselling" in title_text.lower() or "option" in title_text.lower():
            tag = "Counselling"
            color = "#7C3AED" # Purple
            bg = "#F5F0FF"
            icon = "🖥️"
        elif "date" in title_text.lower() or "extended" in title_text.lower() or "deadline" in title_text.lower():
            tag = "Urgent Alert"
            color = "#DC2626" # Red
            bg = "#FFF0F0"
            icon = "🚨"

        article_obj = {
            "id": int(datetime.now().strftime("%y%m%d")) + idx + 100, # Generate unique ID
            "icon": icon,
            "color": color,
            "bg": bg,
            "tag": tag,
            "title": title_text[:85], # Keep headline clean and concise
            "date": "Today's Update",
            "publishedAt": pub_date,
            "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=400&q=80",
            "description": f"Official update regarding {title_text}. Students are advised to log into the official examination portal immediately to check their status, download memos, and complete required admission procedures before the deadline.",
            "eligibility": "Qualified entrance exam candidates with valid intermediate / Plus Two academic records.",
            "applyLink": link_text,
            "courses": courses,
            "state": state
        }
        new_articles.append(article_obj)
        
    return new_articles

def update_json_file(new_articles):
    file_path = 'src/data/NewsData.json'
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    else:
        existing_data = []
        
    # Prevent duplicate entries by checking existing titles
    existing_titles = [item['title'].lower() for item in existing_data]
    added_count = 0
    
    for article in new_articles:
        if article['title'].lower() not in existing_titles:
            existing_data.append(article)
            added_count += 1
            
    # Sort the combined list chronologically by publishedAt (Newest first)
    existing_data.sort(key=lambda x: x['publishedAt'], reverse=True)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, indent=2, ensure_ascii=False)
        
    print(f"Success! Added {added_count} new updates to {file_path}.")

if __name__ == "__main__":
    latest = fetch_latest_news()
    update_json_file(latest)