import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import re
import time
import os
import boto3
from datetime import datetime

# --- CONFIGURATION ---
# 1. Add these in AWS Lambda -> Configuration -> Environment Variables
# Key: GEMINI_API_KEY, Value: Your AI Key
# Key: SNS_TOPIC_ARN, Value: Your SNS Topic ARN (arn:aws:sns:...)
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN')

# Your Interest Profile
USER_INTERESTS = "Unexplained Mysteries, Historical Curiosities, Scientific Facts, True Crime, Weird News, Lendas Urbanas"

# The Curiosities Feed List
RSS_FEEDS = [
    # --- REDDIT (Inglês - Melhores para Shorts Visuais) ---
    "https://www.reddit.com/r/Damnthatsinteresting/top/.rss?t=day",
    "https://www.reddit.com/r/todayilearned/top/.rss?t=day",
    "https://www.reddit.com/r/ExplainLikeImFive/top/.rss?t=day",
    "https://www.reddit.com/r/Creepy/top/.rss?t=day",
    "https://www.reddit.com/r/OddlyTerrifying/top/.rss?t=day",
    "https://www.reddit.com/r/BeAmazed/top/.rss?t=day",

    # --- CURIOSIDADES EM INGLÊS ---
    "https://listverse.com/feed/",
    "https://www.boredpanda.com/feed/",
    "https://www.thefactsite.com/feed/",
    "https://www.mentalfloss.com/rss.xml",
    "https://www.smithsonianmag.com/rss/smart-news/",
    "https://www.livescience.com/feeds/all",
    "https://www.damninteresting.com/feed/",

    # --- BRASILEIROS (Curiosidades, História e Ciência) ---
    "https://super.abril.com.br/feed/",
    "https://super.abril.com.br/mundo-estranho/feed/",
    "https://gizmodo.uol.com.br/feed/",
    "https://aventurasnahistoria.com.br/feed/",
    
    # SUBSTITUTO: Canaltech Ciência (Excelente para Espaço/Astronomia/Descobertas)
    "https://canaltech.com.br/rss/ciencia/",
]

def fetch_rss_items(url):
    print(f"Fetching {url}...")
    items = []
    # Disguise as Chrome
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.google.com/', # Finge que veio do Google
        'Upgrade-Insecure-Requests': '1',
        'Connection': 'keep-alive'
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            try:
                root = ET.fromstring(response.read())
                entries = root.findall('.//item') + root.findall('.//{http://www.w3.org/2005/Atom}entry')
                
                # Fetch 15 items per feed for a good pool
                for item in entries[:15]: 
                    title = item.find('title').text if item.find('title') is not None else "No Title"
                    link_obj = item.find('link')
                    if link_obj is not None:
                        link = link_obj.text if link_obj.text else link_obj.get('href')
                    else:
                        link = "#"
                    items.append({"title": title, "link": link})
            except:
                print(f"  -> XML Parse failed for {url}")
    except Exception as e:
        print(f"  -> Connection failed: {e}")
        
    return items

def rank_articles_with_gemini(articles):
    titles_list = "\n".join([f"{i}. {a['title']}" for i, a in enumerate(articles)])
    
    prompt = f"""
    You are a content curator. Rate these articles from 0 to 100 based on: {USER_INTERESTS}.
    Return ONLY a JSON object in this exact format: 
    {{ "scores": [ {{ "index": 0, "score": 85 }}, {{ "index": 1, "score": 10 }} ] }}
    
    ARTICLES:
    {titles_list}
    """
    
    # Using the verified model
    model_name = "gemini-2.5-flash" 
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={GEMINI_API_KEY}"
    
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            if 'candidates' in result and result['candidates']:
                raw_text = result['candidates'][0]['content']['parts'][0]['text']
                clean_text = re.sub(r"```json|```", "", raw_text).strip()
                
                json_start = clean_text.find('{')
                json_end = clean_text.rfind('}') + 1
                if json_start != -1:
                    clean_text = clean_text[json_start:json_end]
                
                return json.loads(clean_text).get('scores', [])
            return []
    except Exception as e:
        print(f"AI Error: {e}")
        return []

def lambda_handler(event, context):
    print("--- STARTING AGENT ---")
    
    # 1. Validation
    if not GEMINI_API_KEY or not SNS_TOPIC_ARN:
        return {'statusCode': 500, 'body': 'Error: Missing Environment Variables (GEMINI_API_KEY or SNS_TOPIC_ARN)'}

    all_articles = []

    # 2. Fetch all feeds
    for feed in RSS_FEEDS:
        all_articles.extend(fetch_rss_items(feed))
        
    print(f"Collected {len(all_articles)} articles.")

    if not all_articles:
        return {'statusCode': 200, 'body': 'No articles found.'}

    # 3. AI Ranking
    print("Asking AI to rank...")
    scores = rank_articles_with_gemini(all_articles) 
    
    ranked = []
    for s in scores:
        if s['index'] < len(all_articles):
            art = all_articles[s['index']]
            art['score'] = s['score']
            ranked.append(art)
            
    # Sort Top 20 Descending
    ranked.sort(key=lambda x: x.get('score', 0), reverse=True)
    top_20 = ranked[:20]
    
    # 4. Format Email
    date_str = datetime.now().strftime('%Y-%m-%d')
    email_body = f"DAILY CURIOSITIES TOP 20 - {date_str}\n"
    email_body += "="*40 + "\n\n"
    
    for i, art in enumerate(top_20, 1):
        email_body += f"{i}. [{art.get('score',0)}] {art['title']}\n"
        email_body += f"   {art['link']}\n\n"
        
    print(email_body)

    # 5. Send via SNS
    try:
        sns = boto3.client('sns')
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=f"Top 20 Curiosities - {date_str}",
            Message=email_body
        )
        return {'statusCode': 200, 'body': 'Success! Email sent.'}
    except Exception as e:
        print(f"SNS Error: {e}")
        return {'statusCode': 500, 'body': f"Error sending email: {e}"}
