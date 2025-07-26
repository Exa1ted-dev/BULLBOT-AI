from reddit_bot import reddit, scrape_reddit_posts, find_fake_post, reply
from ai_services import tavily_search, generate_reply
from database_handler import save_reply

# Scrape some new Reddit posts
subreddits = reddit.subreddit("conspiracy") # Subreddits to scrape posts from
post_details = [] # List of posts scraped
max_posts = 15 # How many posts to scrape per loop
post_details = scrape_reddit_posts(subreddits, post_details, max_posts)

# Determine the most likely fake post of all scraped
is_fake_buffer = 0.8 # Must have greater than 80% confidence to be considered fake
chosen_post_index = find_fake_post(post_details, is_fake_buffer)

# Search google for relevant articles to correct the post claim
articles = tavily_search(post_details[chosen_post_index]['title'])

# Send Reddit post and article context to Hugging Face Space to generate a final reply
post_reply = generate_reply(chosen_post_index, post_details, articles)['response']

# Reply to the post with a detailed and cited correction
reply(post_details, chosen_post_index, post_reply)

# Save reply details in external database
success = save_reply(post_details[chosen_post_index]['subreddit'],
                     post_details[chosen_post_index]['id'],
                     post_details[chosen_post_index]['title'],
                     post_reply
                     )

if success:
    print("Reply saved to Supabase successfully!")
else:
    print("Reply already exists or failed to save.")

# Future possibilities:
# Switch to tiktoken tokenizer over huggingface to decrease processing time
# Add image processing from posts for further context and more accurate analysis + can analyze image only posts
# Add dashboard to view all responses created by the bot to date
# Find a way to use more powerful models and reply to more posts per month - more impact
