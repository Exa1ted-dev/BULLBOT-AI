import praw
import time
import os
import requests
import pandas as pd
from dotenv import load_dotenv

#region #------------------------------------- BEGIN LOAD ENVIRONMENT VARIABLES -------------------------------------#

# Load environment variables from .env
load_dotenv()
# Reddit
CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
USER_AGENT = os.getenv('REDDIT_USER_AGENT')
USERNAME = os.getenv('REDDIT_USERNAME')
PASSWORD = os.getenv('REDDIT_PASSWORD')
# Tavily
TAVILY_API_KEY  = os.getenv('Tavily_API_KEY')
# Hugging Face
HF_API_KEY = os.getenv('HF_API_KEY')

#endregion #------------------------------------- END LOAD ENVIRONMENT VARIABLES ------------------------------------#

#region #----------------------------------------- BEGIN METHOD DEFINITIONS -----------------------------------------#

# Search google for current, relevant sources to base responses on
def tavily_search(query):
    tavily_url = 'https://api.tavily.com/search'
    headers = {'Authorization': f'Bearer {TAVILY_API_KEY}'}
    payload = {
        'query': query,
        'search_depth': 'advanced',
        'max_results': 3,
        'include_answer': True,
        'include_raw_content': True,
    }

    response = requests.post(tavily_url, json=payload, headers=headers)
    data = response.json()

    # Return summarized answser w/ citations and article mini summary
    return {
        'answer': data.get('answer', ''),
        'citations': [
            {
                'url': c['url'],
                'title': c.get('title', ''),
                'snippet': c.get('snippet') or c.get('content', '')[:500]
            }
            for c in data.get('citations', [])
        ]
    }
    
# Access Hugging Face Spaces classification model to determine whether a post is likely true or false
def classify_post_truth(post_title, post_body):
    hf_classify_url = 'https://Exa1ted-dev-BULLBOT-Post-Classification.hf.space/predict'
    full_text = f'Title: {post_title}\n\nBody: {post_body}'
    payload = {'text': full_text}

    try:
        response = requests.post(hf_classify_url, json=payload)
        response.raise_for_status() # Raise error if not status 200
        result = response.json()
        return result # {'label': 'FAKE', 'confidence': 0.968}
    except requests.RequestException as e:
        print(f'Error during post classification request: {e}')
        return None

# Find the scraped post with highest likelihood of being fake
def find_fake_post(post_details, is_fake_buffer):
    post_confidence_levels = []
    fakest_post_index = -1

    # Classify all posts and store confidence levels
    for i in range(len(post_details)):
        post_confidence_levels.append(classify_post_truth(post_details[i]['title'], post_details[i]['body_text']))

    # Cycle through posts to find final fakest choice
    for i in range(len(post_confidence_levels)):
        if post_confidence_levels[i][0]['label'] == 'LABEL_0':
            if post_confidence_levels[i][0]['score'] >= is_fake_buffer:
                if fakest_post_index < 0:
                    fakest_post_index = i
                elif post_confidence_levels[i][0]['score'] > post_confidence_levels[fakest_post_index][0]['score']:
                    fakest_post_index = i
    
    if fakest_post_index == -1:
        return None
    else:
        return fakest_post_index

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

#endregion #---------------------------------------- END METHOD DEFINITIONS -----------------------------------------#

#region #------------------------------------- BEGIN BULLBOT POST ANALYSIS CODE -------------------------------------#

# Create reddit bot
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    username=USERNAME,
    password=PASSWORD,
    user_agent=USER_AGENT
)

# Scrape some new Reddit posts
# Maybe filter out posts with too many words - prevents problems down the line like a cut off post being passed to the final model for analysis
subreddits = reddit.subreddit("conspiracy") # Subreddits to scrape posts from
post_details = [] # List of posts scraped
max_posts = 15 # How many posts to scrape per loop
post_details = scrape_reddit_posts(subreddits, post_details, max_posts)

# Determine the most likely fake post of all scraped
is_fake_buffer = 0.8 # Must have greater than 80% confidence to be considered fake
chosen_post_index = find_fake_post(post_details, is_fake_buffer)

# Search google for relevant articles to correct the post claim
articles = tavily_search(post_details[chosen_post_index]['title'])

# Pass post details and relevant context articles to AI model to correct

# Reply to the post with a detailed and cited correction

# Potentially save response to an external database for later review and display in a dashboard

#endregion #------------------------------------ END BULLBOT POST ANALYSIS CODE -------------------------------------#
