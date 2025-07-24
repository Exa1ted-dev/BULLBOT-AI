import praw
import time
import os
import requests
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Reddit
CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
USER_AGENT = os.getenv('REDDIT_USER_AGENT')
USERNAME = os.getenv('REDDIT_USERNAME')
PASSWORD = os.getenv('REDDIT_PASSWORD')
# SerpAPI
SERP_API_KEY  = os.getenv('SERP_API_KEY')
# Hugging Face
HF_API_KEY = os.getenv('HF_API_KEY')


# Search google for current, relevant sources to base responses on
def search_serpapi(query, num_results=5):
    serpapi_url = 'https://serpapi.com/search'
    params = {
        'q': query,
        'api_key': SERP_API_KEY,
        'num': num_results,
        'engine': 'google',
    }

    # Gather data from google search
    response = requests.get(serpapi_url, params=params)
    data = response.json()

    # Format search results to use as AI response context
    results = []
    for result in data.get('organic_results', [])[:num_results]:
        snippet = result.get('snippet', '')
        title = result.get("title", "")
        link = result.get("link", "")
        results.append(f"{title}\n{snippet}\n{link}")

    return '\n\n'.join(results)



def detect_fake_news(post_title, post_body):
    hf_url = 'https://api-inference.huggingface.co/models/jy46604790/Fake-News-Bert-Detect'
    headers = {
        'Authorization': f'Bearer {HF_API_KEY}'
    }

    combined_input = f"Title: {post_title}\n\nBody: {post_body}"
    payload = {
        'inputs': combined_input
    }

    try:
        response = requests.post(hf_url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        if isinstance(result, list):
            return result
        else:
            return 'ERROR', 0.0
    except Exception as e:
        print("Inference error: ", e)
        return 'ERROR', 0.0



def calculate_misinformation_chance(false_chance, true_chance):
    return false_chance - true_chance



# Scrape Reddit posts
def scrape_reddit_posts(subreddits, post_details, max_posts):
    post_count = 0 # No scraped posts yet this loop

    # Listen to new posts in specified subreddits
    for post in subreddits.stream.submissions(skip_existing=True):
        try:
            # Store scraped posts
            post_details.append({
                'title': post.title,
                'author': str(post.author),
                'body_text': post.selftext,
                'url': post.url,
                'permalink': post.permalink,
            })

            # Keep track of how many posts we have scraped during the loop
            post_count += 1
            if post_count >= max_posts:
                break

            # Pause to avoid hitting Reddit too fast
            time.sleep(2)

        except Exception as e:
            print(f"Error reading post: {e}")
            time.sleep(5)

    return post_details



# Create reddit bot
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    username=USERNAME,
    password=PASSWORD,
    user_agent=USER_AGENT
)

# Scrape some new Reddit posts
subreddits = reddit.subreddit("conspiracy") # Subreddits to scrape posts from
post_details = [] # List of posts scraped
max_posts = 15 # How many posts to scrape per loop

post_details = scrape_reddit_posts(subreddits, post_details, max_posts)


# Determine the most likely fake post of all scraped
post_confidence_levels = []
post_misinformation_chances = []
fakest_post_index = 0
for i in range(len(post_details)):
    post_confidence_levels.append(detect_fake_news(post_details[i]['title'], post_details[i]['body_text']))
    post_misinformation_chances.append(calculate_misinformation_chance(post_confidence_levels[i][0, post_confidence_levels[i][1]]))

for i in range(len(post_misinformation_chances)):
    if post_misinformation_chances[i] >= post_misinformation_chances[fakest_post_index]:
        fakest_post_index = i

# Search google for relevant articles to correct the fakest post


# Further summarize and extract article details

# Pass post details and relevant context articles to AI model to correct

# Reply to the post with a detailed and cited correction

# Potentially save response to an external database for later review and display in a dashboard
