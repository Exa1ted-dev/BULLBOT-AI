from reddit_bot import reddit, scrape_reddit_posts, find_fake_post, reply
from ai_services import generate_reply, serpapi_search
from database_handler import save_reply

# Scrape some new Reddit posts
print('begin scrape\n')
subreddits = reddit.subreddit("conspiracy+conspiracy_commons+antiVaxxers+COVID19_conspiracy+alternativehealth+WallStreetBets+FlatEarth+woo") # Subreddits to scrape posts from
post_details = [] # List of posts scraped
max_posts = 10 # How many posts to scrape per loop
#post_details = scrape_reddit_posts(subreddits, post_details, max_posts)
#test
post_details.append({
                'id': 'testid123',
                'title': 'Nasa confirms climate change is false',
                'body_text': 'I KNEW IT!!',
                'url': 'Notarealurl.com',
                'permalink': 'nolink',
                'subreddit': 'conspiracy'
            })

# Determine the most likely fake post of all scraped
print('begin classify\n')
is_fake_buffer = 0.92 # Must have greater than 92% confidence to be considered fake
chosen_post_index = find_fake_post(post_details, is_fake_buffer)

# Search google for relevant articles to correct the post claim
print('begin search\n')
articles = serpapi_search(post_details[chosen_post_index]['title'])
print(articles)
print('\n')

# Send Reddit post and article context to Hugging Face Space to generate a final reply
print('begin generate reply\n')
post_reply = generate_reply(chosen_post_index, post_details, articles)
print(post_reply)
print('\n')

# # Reply to the post with a detailed and cited correction
# print('begin comment\n')
# reply(post_details, chosen_post_index, post_reply)

# # Save reply details in external database
# print('begin db store\n')
# success = save_reply(post_details[chosen_post_index]['subreddit'],
#                      post_details[chosen_post_index]['id'],
#                      post_details[chosen_post_index]['title'],
#                      post_reply
#                      )

# if success:
#     print("Reply saved to Supabase successfully!")
# else:
#     print("Reply already exists or failed to save.")

# Future possibilities:
# Switch to tiktoken tokenizer over huggingface to decrease processing time
# Add image processing from posts for further context and more accurate analysis + can analyze image only posts
# Add dashboard to view all responses created by the bot to date
# Find a way to use more powerful models and reply to more posts per month - more impact
# Newspaper3k article summaries
# Increase summary length - detail  -accuracy
