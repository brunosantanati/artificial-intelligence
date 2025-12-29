import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import re
import os
import boto3
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

# --- CONFIGURATION ---
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN')

USER_INTERESTS = "Unexplained Mysteries, Historical Curiosities, Scientific Facts, True Crime, Weird News, Lendas Urbanas"

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

# --- HELPERS ---
def parse_date(date_str):
    """Parses date and forces UTC to prevent offset-naive/aware errors."""
    if not date_str:
        return datetime(1970, 1, 1, tzinfo=timezone.utc)
    try:
        dt = parsedate_to_datetime(date_str)
        if dt.tzinfo is None: dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except:
        try:
            clean_date = date_str.replace('Z', '+00:00')
            dt = datetime.fromisoformat(clean_date)
            if dt.tzinfo is None: dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc)
        except:
            return datetime(1970, 1, 1, tzinfo=timezone.utc)

def fetch_rss_items(url):
    items = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0'}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            root = ET.fromstring(response.read())
            entries = root.findall('.//item') + root.findall('.//{http://www.w3.org/2005/Atom}entry')
            for item in entries:
                title = item.findtext('title') or item.findtext('{http://www.w3.org/2005/Atom}title') or "No Title"
                
                # Logic for Reddit/Atom Links vs Standard RSS
                link = "#"
                link_node = item.find('{http://www.w3.org/2005/Atom}link')
                if link_node is not None:
                    link = link_node.get('href')
                else:
                    link = item.findtext('link') or "#"

                raw_date = (item.findtext('pubDate') or 
                            item.findtext('{http://www.w3.org/2005/Atom}published') or 
                            item.findtext('{http://www.w3.org/2005/Atom}updated'))
                
                items.append({
                    "title": title, 
                    "link": link, 
                    "date": parse_date(raw_date)
                })
    except:
        pass
    return items

def rank_articles_with_gemini(articles):
    titles_payload = ""
    for i, a in enumerate(articles):
        titles_payload += f"ID:{i} | {a['title']}\n"

    prompt = f"""
    Rate these articles from 0 to 100 based on these interests: {USER_INTERESTS}.
    Return ONLY a JSON object in this exact format:
    {{ "scores": [ {{ "id": 0, "score": 85 }}, {{ "id": 1, "score": 10 }} ] }}
    
    ARTICLES:
    {titles_payload}
    """

    model_name = "gemini-2.5-flash" 
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={GEMINI_API_KEY}"
    
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            raw_text = result['candidates'][0]['content']['parts'][0]['text']
            clean_text = re.sub(r"```json|```", "", raw_text).strip()
            return json.loads(clean_text).get('scores', [])
    except Exception as e:
        print(f"AI Error: {e}")
        return []

def lambda_handler(event, context):
    if not GEMINI_API_KEY or not SNS_TOPIC_ARN:
        return {'statusCode': 500, 'body': 'Missing Environment Variables'}

    all_articles = []
    for feed in RSS_FEEDS:
        all_articles.extend(fetch_rss_items(feed))

    # 1. SORT BY DATE FIRST
    all_articles.sort(key=lambda x: x['date'], reverse=True)

    # 2. SELECT 100 MOST RECENT
    top_100_pool = all_articles[:100]

    if not top_100_pool:
        return {'statusCode': 200, 'body': 'No articles found.'}

    # 3. RANK ONLY THE 100
    scores = rank_articles_with_gemini(top_100_pool)
    
    score_map = {item.get('id'): item.get('score', 0) for item in scores}
    for i, art in enumerate(top_100_pool):
        art['score'] = score_map.get(i, 0)

    # 4. ORDER BY RELEVANCE
    top_100_pool.sort(key=lambda x: x.get('score', 0), reverse=True)

    # 5. FORMAT EMAIL
    date_now = datetime.now().strftime('%Y-%m-%d')
    email_body = f"DAILY RANKED CURIOSITIES - {date_now}\n"
    email_body += "="*50 + "\n\n"
    
    for i, art in enumerate(top_100_pool, 1):
        email_body += f"{i}. [{art['score']}/100] {art['title']}\n"
        email_body += f"   Published: {art['date'].strftime('%H:%M UTC')}\n"
        email_body += f"   Link: {art['link']}\n\n"

    # 6. SEND VIA SNS
    try:
        sns = boto3.client('sns')
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=f"Top Curiosities Ranked - {date_now}",
            Message=email_body
        )
        return {'statusCode': 200, 'body': 'Success: Ranked articles sent via SNS.'}
    except Exception as e:
        print(f"SNS Error: {e}")
        return {'statusCode': 500, 'body': f"Error: {e}"}
