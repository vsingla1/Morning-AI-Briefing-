import requests
import json
import os # <--- ADD THIS LINE
from datetime import datetime, timedelta
from groq import Groq

# ==========================================
# ⚙️ CONFIGURATION & API KEYS
# ==========================================
# We are now fetching keys securely from the hidden environment!
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

# Initialize the Groq client
client = Groq(api_key=GROQ_API_KEY)

# ==========================================
# 1. THE EYES (Fetch News)
# ==========================================
def get_top_ai_news():
    """Fetches the latest AI news articles from NewsAPI."""
    print("🕵️‍♂️ Step 1: Scanning the internet for AI news...")
    
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    url = "https://newsapi.org/v2/everything"
    
    params = {
        "q": '"Artificial Intelligence" OR "Generative AI"',
        "from": yesterday,
        "sortBy": "popularity",
        "language": "en",
        "apiKey": NEWS_API_KEY
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        articles = response.json().get("articles", [])[:5]
        extracted_news = ""
        for article in articles:
            title = article.get("title")
            description = article.get("description")
            link = article.get("url")
            if title and description:
                extracted_news += f"Title: {title}\nSummary: {description}\nLink: {link}\n\n"
        return extracted_news
    else:
        print(f"❌ Failed to fetch news. Error: {response.status_code}")
        return None

# ==========================================
# 2. THE BRAIN (Summarize with Groq)
# ==========================================
def summarize_news(raw_news_text):
    """Sends raw news text to the Groq LLM to format for Slack."""
    print("🧠 Step 2: Groq is analyzing and summarizing...")
    
    prompt = f"""
    You are an expert AI tech analyst. I will provide you with 5 recent news articles about Artificial Intelligence.
    Your job is to read them and write a highly engaging, 5-minute daily brief for my Slack channel.
    
    Formatting rules for Slack:
    - Use a catchy headline with emojis.
    - Use bullet points for each news item.
    - Keep each bullet point to 3-4 short sentences. Get straight to the point.
    - Use *bold text* for company names or key terms.
    - IMPORTANT: After each bullet point, include the original article link on a new line formatted as: Read more: <link>
    - Add a tiny "Thought of the day" or quick takeaway at the very end.
    
    Here is the raw news data:
    {raw_news_text}
    """
    
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant",
    )
    
    return response.choices[0].message.content

# ==========================================
# 3. THE MOUTH (Send to Slack)
# ==========================================
def send_slack_message(text):
    """Sends the final summary to your Slack channel."""
    print("🚀 Step 3: Delivering briefing to Slack...")
    
    payload = {"text": text}
    response = requests.post(
        SLACK_WEBHOOK_URL, 
        data=json.dumps(payload),
        headers={'Content-Type': 'application/json'}
    )
    
    if response.status_code == 200:
        print("✅ Success! Check your Slack channel.")
    else:
        print(f"❌ Failed to send message. Error: {response.status_code}")

# ==========================================
# 🏃‍♂️ MAIN AGENT EXECUTION
# ==========================================
if __name__ == "__main__":
    print("🤖 Good morning! Starting the AI Agent Pipeline...\n")
    
    # 1. Get News
    news_data = get_top_ai_news()
    
    if news_data:
        # 2. Summarize News
        final_summary = summarize_news(news_data)
        
        # 3. Send to Slack
        send_slack_message(final_summary)
    else:
        print("Pipeline aborted: No news data found.")

