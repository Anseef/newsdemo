def fetch_latest_news():
    print("1. Contacting Google News RSS...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    # Using when:7d to ensure we find articles!
    rss_url = "https://news.google.com/rss/search?q=(KEAM+OR+TNEA+OR+EAMCET+OR+COMEDK+OR+KCET)+education+when:7d&hl=en-IN&gl=IN&ceid=IN:en"
    
    response = requests.get(rss_url, headers=headers)
    print(f"2. Google responded with Status Code: {response.status_code}")
    
    soup = BeautifulSoup(response.content, features="html.parser")
    items = soup.findAll('item')
    print(f"3. Found {len(items)} total articles in the RSS feed.")
    
    new_articles = []
    
    for idx, item in enumerate(items[:8]):  # Check top 8 articles
        title_text = item.title.text.split(" - ")[0]
        link_text = item.link.text
        pub_date = datetime.now().strftime("%Y-%m-%d")
        
        print(f"   -> Scraping: {title_text[:50]}...")
        
        article_obj = {
            "id": int(datetime.now().strftime("%y%m%d")) + idx + 100,
            "icon": "🎓",
            "color": "#1B6CA8",
            "bg": "#EBF5FF",
            "tag": "News Update",
            "title": title_text[:85],
            "date": "Recent Update",
            "publishedAt": pub_date,
            "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=400&q=80",
            "description": f"Official update regarding {title_text}. Students are advised to log into the official examination portal to verify their status and complete required procedures.",
            "eligibility": "Qualified entrance exam candidates with valid Plus Two academic records.",
            "applyLink": link_text,
            "courses": ["B.Tech", "B.Pharm"],
            "state": "South India"
        }
        new_articles.append(article_obj)
        
    return new_articles