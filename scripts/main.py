import praw
import time
import os
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
USER_AGENT = os.getenv('USER_AGENT')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

# Create reddit bot
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    username=USERNAME,
    password=PASSWORD,
    user_agent=USER_AGENT
)

# Monitor posts
print("Listening for posts ...\n")
subreddit = reddit.subreddit("all")

# max_posts = 10
# count = 0
post_details = []

# Listen to new posts in specified subreddit until we reach max capacity
for post in subreddit.stream.submissions(skip_existing=True):
    try:
        # Store scraped posts
        post_details.append({
            'title': post.title,
            'author': str(post.author),
            'body_text': post.selftext,
            'url': post.url,
            'permalink': post.permalink
        })

        # count += 1
        # if count >= max_posts:
        #     break

        # Pause to avoid hitting Reddit too fast
        time.sleep(2)

    except Exception as e:
        print(f"Error reading post: {e}")
        time.sleep(5)

# Save scraped posts in a CSV file for testing
scraped_posts_df = pd.DataFrame(post_details)
scraped_posts_df.to_csv('scraped_posts.csv', index=False)
