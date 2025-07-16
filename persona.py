import os, re, textwrap, datetime, collections, pathlib
from dotenv import load_dotenv
import praw, spacy

# ─── Load environment variables ───
load_dotenv()
reddit = praw.Reddit(
    client_id     = os.getenv("REDDIT_CLIENT_ID"),
    client_secret = os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent    = os.getenv("REDDIT_USER_AGENT")
)
nlp = spacy.load("en_core_web_sm")
OUT_DIR = pathlib.Path("output")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ─── Utility functions ───
def collect(username, lim_c=100, lim_s=30):
    user = reddit.redditor(username)
    comments = list(user.comments.new(limit=lim_c))
    submissions = list(user.submissions.new(limit=lim_s))
    return comments, submissions

def top_entities(texts, labels=("GPE", "ORG", "PERSON", "NORP"), n=5):
    doc = nlp(" ".join(texts))
    freq = collections.Counter(ent.text for ent in doc.ents if ent.label_ in labels)
    return [w for w, _ in freq.most_common(n)]

def sentiment(text):
    pos = len(re.findall(r"\b(love|great|awesome|happy|thanks?)\b", text, flags=re.I))
    neg = len(re.findall(r"\b(hate|terrible|awful|angry|sad|annoy|sucks)\b", text, flags=re.I))
    return pos - neg

# ─── HTML generator ───
def generate_html(username, comments, submissions):
    texts = [c.body for c in comments] + [s.title + " " + (s.selftext or "") for s in submissions]
    ents = top_entities(texts)
    senti = sentiment(" ".join(texts))
    tone = "Positive" if senti > 5 else "Negative" if senti < -5 else "Mixed"
    location = ', '.join(ents) if ents else "Not found"
    top_subs = collections.Counter(c.subreddit.display_name for c in comments).most_common(5)

    def comment_block(qs, limit=3):
        blocks = []
        for c in qs:
            if len(blocks) >= limit: break
            text = c.body.strip().replace("\n", " ")[:160]
            blocks.append(f'<blockquote>{text}...<br><a href="https://reddit.com{c.permalink}">View</a></blockquote>')
        return "\n".join(blocks)

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Reddit Persona - u/{username}</title>
    <style>
        body {{
            font-family: 'Segoe UI', sans-serif;
            max-width: 900px;
            margin: 40px auto;
            padding: 20px;
            line-height: 1.6;
            background: #fff8f3;
            color: #333;
            border: 2px solid #ef8a42;
            border-radius: 16px;
        }}
        h1, h2 {{
            color: #d35400;
            border-bottom: 2px solid #ef8a42;
            padding-bottom: 4px;
        }}
        .persona-section {{ margin-bottom: 32px; }}
        .bar {{ display: inline-block; background: #ef8a42; height: 12px; margin-right: 6px; }}
        blockquote {{
            margin: 8px 0;
            padding-left: 12px;
            border-left: 4px solid #ef8a42;
            color: #555;
        }}
        a {{ color: #e67e22; }}
    </style>
</head>
<body>
    <h1>👤 Reddit User Persona: u/{username}</h1>
    <p><strong>Generated:</strong> {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</p>

    <div class="persona-section">
        <h2>🧾 Basic Info</h2>
        <p><strong>Username:</strong> u/{username}</p>
        <p><strong>Location clues:</strong> {location}</p>
        <p><strong>Overall tone:</strong> {tone}</p>
    </div>

    <div class="persona-section">
        <h2>🧠 Personality Snapshot</h2>
        <p>Sentiment Score: {senti}</p>
        <p>Most active subreddits:</p>
        <ul>
            {''.join(f"<li>r/{sr}</li>" for sr, _ in top_subs)}
        </ul>
    </div>

    <div class="persona-section">
        <h2>😤 Complaints / Rants</h2>
        {comment_block([c for c in comments if any(w in c.body.lower() for w in ["hate","can't","don't","terrible","annoy","sucks"])])}
    </div>

    <div class="persona-section">
        <h2>🔗 Sample Comments</h2>
        {comment_block(comments)}
    </div>

    <footer style="text-align:center; margin-top:40px; font-size: 0.9em;">
        <p>Reddit persona builder • 2025</p>
    </footer>
</body>
</html>
"""
    return html

# ─── Main runner ───
def run_persona():
    profile_url = input("🔗 Enter a Reddit profile URL (e.g. https://www.reddit.com/user/someuser/): ").strip()
    if not re.match(r"https?://(www\.)?reddit\.com/user/[\w\-\_]+/?$", profile_url):
        print("❌ Invalid Reddit profile URL.")
        return
    username = profile_url.rstrip("/").split("/")[-1]
    print(f"🔍 Scraping u/{username}...")
    try:
        comments, submissions = collect(username)
    except Exception as e:
        print(f"❌ Failed to fetch data: {e}")
        return
    if not comments:
        print("🚫 No public comments or posts found.")
        return

    html = generate_html(username, comments, submissions)
    html_path = OUT_DIR / f"persona_{username}.html"
    html_path.write_text(html, encoding="utf-8")
    print(f"✅ HTML persona created → {html_path.absolute()}")
    print(f"📂 Open in browser or convert to PDF as needed.")

if __name__ == "__main__":
    run_persona()
