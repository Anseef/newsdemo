import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
from newspaper import Article  # Import the article extractor

RSS_URL = "https://news.google.com/rss/search?q=(KEAM+OR+TNEA+OR+EAMCET+OR+COMEDK+OR+KCET)+education+when:1d&hl=en-IN&gl=IN&ceid=IN:en"

def extract_article_details(url):
    """Visits the news link and extracts full text and images."""
    try:
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()  # Built-in keyword and summary extraction
        
        # Return the extracted details
        return {
            "summary": article.summary if article.summary else article.text[:250] + "...",
            "full_text": article.text,
            "image": article.top_image if article.top_image else "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=400&q=80"
        }
    except Exception as e:
        print(f"Could not extract details from {url}: {e}")
        return {
            "summary": "Please click the link below to read the full official notification.",
            "full_text": "",
            "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=400&q=80"
        }

def fetch_latest_news():
    print("Fetching live RSS feed...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(RSS_URL, headers=headers)
    soup = BeautifulSoup(response.content, features="html.parser")
    items = soup.findAll('item')
    
    new_articles = []
    
    for idx, item in enumerate(items[:4]):
        title_text = item.title.text.split(" - ")[0]
        link_text = item.link.text
        pub_date = datetime.now().strftime("%Y-%m-%d")
        
        print(f"Deep scraping: {title_text[:40]}...")
        
        # 1. FETCH DEEP DETAILS HERE
        details = extract_article_details(link_text)
        
        # 2. Build your JSON Object using the extracted data
        article_obj = {
            "id": int(datetime.now().strftime("%y%m%d")) + idx + 100,
            "icon": "🎓",
            "color": "#1B6CA8",
            "bg": "#EBF5FF",
            "tag": "News Update",
            "title": title_text[:85],
            "date": "Today's Update",
            "publishedAt": pub_date,
            "image": details["image"],                 # Real extracted news image!
            "description": details["summary"][:200],   # Real extracted summary!
            "fullText": details["full_text"][:1000],   # Deeper reading text
            "eligibility": "Refer to official notification for complete educational criteria.",
            "applyLink": link_text,
            "courses": ["B.Tech", "B.E"],
            "state": "South India"
        }
        new_articles.append(article_obj)
        
    return new_articles