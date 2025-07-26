import time
import praw
import ai_services
import config

# Load environment variables
CLIENT_ID = config.CLIENT_ID
CLIENT_SECRET = config.CLIENT_SECRET
USER_AGENT = config.USER_AGENT
USERNAME = config.USERNAME
PASSWORD = config.PASSWORD

# Create reddit bot
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    username=USERNAME,
    password=PASSWORD,
    user_agent=USER_AGENT
)

# Find the scraped post with highest likelihood of being fake
def find_fake_post(post_details, is_fake_buffer):
    post_confidence_levels = []
    fakest_post_index = -1

    # Classify all posts and store confidence levels
    for i in range(len(post_details)):
        post_confidence_levels.append(ai_services.classify_post_truth(post_details[i]['title'], post_details[i]['body_text']))

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
            # Check approximate post text token size
            combined_text = f'{post.title} {post.selftext}'
            approx_token_count = len(combined_text) // 4

            # Ignore posts over 450 tokens -> they will be too big to easily analyze with AI later
            if approx_token_count > 450:
                continue

            # Store scraped posts
            post_details.append({
                'id': post.id,
                'title': post.title,
                'body_text': post.selftext,
                'url': post.url,
                'permalink': post.permalink,
                'subreddit': post.subreddit.display_name
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

# Reply to the post
def reply(post_details, post_index, post_reply):
    submission = reddit.submission(url=f'https://www.reddit.com{post_details[post_index]['permalink']}')
    submission.reply(post_reply)
