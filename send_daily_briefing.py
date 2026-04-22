import feedparser
import smtplib
import pytz
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from jinja2 import Template

# --- Define news feeds and categories ---
FEEDS = {
    "AI": "https://news.google.com/rss/search?q=artificial+intelligence",
    "Robotics": "https://news.google.com/rss/search?q=robotics",
    # Add more as needed
}

YOUR_EMAIL = "you@gmail.com"
YOUR_PASSWORD = "password"  # Use App Password if 2FA is enabled
RECIPIENT_EMAIL = "19911162@qq.com"

def fetch_news():
    results = []
    for category, feed_url in FEEDS.items():
        parsed = feedparser.parse(feed_url)
        for entry in parsed.entries[:10]:  # Pull a reasonable amount
            abstract = entry.summary if hasattr(entry, 'summary') else ""
            results.append({
                "category": category,
                "subject": entry.title,
                "abstract": abstract[:400],
                "info_source": entry.get("source", {}).get("title", "Google News"),
                "reference": entry.link,
                "published": entry.get("published_parsed"),
            })
    return results

def rank_and_select(news):
    # Here you can implement more advanced ranking
    news_sorted = sorted(news, key=lambda x: x.get("published", ""), reverse=True)
    # Use further selection/rank logic, NLP model, etc. if desired
    return news_sorted[:25]

def format_email(news_items):
    template = Template("""
    {% for n in news %}
    <b>Category:</b> {{n.category}}<br>
    <b>Subject:</b> {{n.subject}}<br>
    <b>Abstract:</b> {{n.abstract}}<br>
    <b>Info Source:</b> {{n.info_source}}<br>
    <b>Reference:</b> <a href="{{n.reference}}">{{n.reference}}</a><br>
    <hr>
    {% endfor %}
    """)
    return template.render(news=news_items)

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = YOUR_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(YOUR_EMAIL, YOUR_PASSWORD)
        server.send_message(msg)

if __name__ == "__main__":
    news = fetch_news()
    selected_news = rank_and_select(news)
    body = format_email(selected_news)
    send_email(f"Today's Tech & Science Briefing ({datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d')})", body)
