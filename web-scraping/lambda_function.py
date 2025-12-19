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
    "https://www.reddit.com/r/Damnthatsinteresting/top/.rss?t=day",
    "https://www.reddit.com/r/todayilearned/top/.rss?t=day",
    "https://www.reddit.com/r/ExplainLikeImFive/top/.rss?t=day",
    "https://www.reddit.com/r/Creepy/top/.rss?t=day",
    "https://www.reddit.com/r/OddlyTerrifying/top/.rss?t=day",
    "https://www.reddit.com/r/BeAmazed/top/.rss?t=day",
    "https://listverse.com/feed/",
    "https://www.boredpanda.com/feed/",
    "https://www.thefactsite.com/feed/",
    "https://www.mentalfloss.com/rss.xml",
    "https://www.smithsonianmag.com/rss/smart-news/",
    "https://www.livescience.com/feeds/all",
    "https://www.damninteresting.com/feed/",
    "https://super.abril.com.br/feed/",
    "https://super.abril.com.br/mundo-estranho/feed/",
    "https://gizmodo.uol.com.br/feed/",
    "https://aventurasnahistoria.com.br/feed/",
    "https://canaltech.com.br/rss/ciencia/",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UC7zbUfFoMAMGHIRUE8gjVnw", # TechTudo
    "http://astronomy-universo.blogspot.com/feeds/posts/default", # Astronomia e Universo
    "http://www.numaniaticos.com/feed/", # Numaniáticos
    "https://api.reddit.com/subreddit/creepy", # r/creepy
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCVVIVc6DfU8uWJ60vk8iKpQ", # Superinteressante
    "https://www.youtube.com/feeds/videos.xml?channel_id=UChz45Ir-nTCxn7qmJ5nXQ6Q", # GizmodoBR
    "http://www.vocesabia.net/feed/", # Curiosidades no Você Sabia
    "http://super.abril.com.br/blogs/oraculo/feed/", # Oráculo – Super
    "https://hypescience.com/feed/", # HypeScience
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCH2VZQBLFTOp6I_qgnBJCuQ", # Canal Nostalgia
    "http://randomc.net/feed/", # Random Curiosity
    "https://www.youtube.com/feeds/videos.xml?channel_id=UClu474HMt895mVxZdlIHXEA", # Nerdologia
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCunqx90PNIv30uOgn0m4CTg", # Acredite ou Não
    "http://scienceblogs.com.br/colecionadores/feed/", # Colecionadores de Ossos
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCNYaxPiba3oxmeL_3jKxnYA", # Insane Curiosity
    "http://rss.megacurioso.com.br/feed", # Novidades do Mega Curioso
    "http://gdata.youtube.com/feeds/base/users/superinteressanteweb/uploads?alt=rss&v=2&orderby=published&client=ytapi-youtube-profile", # Superinteressante (Legacy API)
    "http://www.insoonia.com/feed", # iNSôÔNiA
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCjcEWCkuafL02yvkujCwL4w", # Colecionadores de Ossos (YT)
    "https://www.youtube.com/feeds/videos.xml?channel_id=UC9li9QbQlmExYM6UxnvhuCQ", # That Creepy Reading
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCj0O6W8yDuLg3iraAXKgCrQ", # Você Sabia?
    "http://canalnostalgia.blogspot.com/feeds/posts/default", # Canal Nostalgia (Blog)
    "http://mundoestranho.abril.com.br/rss", # Mundo Estranho – Super
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCmUVDdwB1_RrQyfu80fvRrw", # Revista Galileu
    "https://www.techtudo.com.br/rss/techtudo/", # techtudo
    "http://gdata.youtube.com/feeds/base/users/iberethenorio/uploads?alt=rss&v=2&orderby=published&client=ytapi-youtube-profile", # Manual do Mundo (Legacy API)
    "http://www.assombrado.com.br/feeds/posts/default", # Assombrado
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCIQPHl1WKKTt9KkWyo_JNig", # INCRÍVEL
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCKHhA5hN2UohhFDfNXB_cvQ", # Manual do Mundo
    "https://psxbrasil.com.br/feed/", # PSX Brasil
    "http://br.ign.com/feed.xml", # IGN Brasil
    "http://gdata.youtube.com/feeds/base/users/canalmegacurioso/uploads?alt=rss&v=2&orderby=published&client=ytapi-youtube-profile", # Mega Curioso (Legacy API)
    "http://misteriosdomundo.org/feed/", # Misterios do Mundo
    "http://www.gizmodo.com.br/feed/", # Gizmodo em português
    "http://www.eltiempo.com/contenido/mundo-curioso/rss.xml", # EL TIEMPO
    "http://spacetoday.com.br/feed/", # SPACE TODAY
    "https://revistagalileu.globo.com/rss/galileu", # galileu
    "http://gdata.youtube.com/feeds/base/users/fecastanhari/uploads?alt=rss&v=2&orderby=published&client=ytapi-youtube-profile", # Canal Nostalgia (Legacy API)
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCsg11Ullu0dBrNXTrDBKOXA", # Mega Curioso
    "http://www.baratonta.com/feeds/posts/default", # Baratonta
    "http://www.bbc.co.uk/portuguese/index.xml", # BBC Brasil
    "http://super.abril.com.br/feed/", # Super
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCn9Erjy00mpnWeLnRqhsA1g", # Ciência Todo Dia
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCvKP7V9o8xfB-hpk3noKAiw", # Acervo do Terror
    "http://www.hypeness.com.br/feed/", # Hypeness
    "https://www.youtube.com/playlist?list=UUn9Erjy00mpnWeLnRqhsA1g" # Ciência Todo Dia (Playlist URL)
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
            
    # Sort Top 100 Descending
    ranked.sort(key=lambda x: x.get('score', 0), reverse=True)
    top_100 = ranked[:100]
    
    # 4. Format Email
    date_str = datetime.now().strftime('%Y-%m-%d')
    email_body = f"DAILY CURIOSITIES TOP 100 - {date_str}\n"
    email_body += "="*40 + "\n\n"
    
    for i, art in enumerate(top_100, 1):
        email_body += f"{i}. [{art.get('score',0)}] {art['title']}\n"
        email_body += f"   {art['link']}\n\n"
        
    print(email_body)

    # 5. Send via SNS
    try:
        sns = boto3.client('sns')
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=f"Top 100 Curiosities - {date_str}",
            Message=email_body
        )
        return {'statusCode': 200, 'body': 'Success! Email sent.'}
    except Exception as e:
        print(f"SNS Error: {e}")
        return {'statusCode': 500, 'body': f"Error sending email: {e}"}
