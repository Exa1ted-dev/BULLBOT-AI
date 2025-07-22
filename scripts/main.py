import praw
import time
import pandas as pd

# Create reddit bot
reddit = praw.Reddit(
    client_id='NEcQn8XXXJSkl3Z4EcC0zQ',
    client_secret='Y-Xd67JMc9e-OFYkqcP_Y0Lps55_WA',
    username='BULLBOT_AI',
    password='HTN_BullBot_2025!!!',
    user_agent='BULLBOT/0.1 by u/BULLBOT_AI'
)

# Monitor posts
print("Listening for posts ...\n")
subreddit = reddit.subreddit("all")

max_posts = 10
count = 0
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

        count += 1
        if count >= max_posts:
            break

        # Pause to avoid hitting Reddit too fast
        time.sleep(2)

    except Exception as e:
        print(f"Error reading post: {e}")
        time.sleep(5)

# Save scraped posts in a CSV file for testing
scraped_posts_df = pd.DataFrame(post_details)
scraped_posts_df.to_csv('scraped_posts.csv', index=False)
