from reddit_bot import reddit, scrape_reddit_posts, find_fake_post, summarize_article, build_prompt, reply
from ai_services import generate_reply, serpapi_search
from database_handler import save_reply

# Scrape some new Reddit posts
print('begin scrape\n')
subreddits = reddit.subreddit("conspiracy_commons+antiVaxxers+COVID19_conspiracy+alternativehealth+WallStreetBets+FlatEarth+woo") # Subreddits to scrape posts from
post_details = [] # List of posts scraped
max_posts = 10 # How many posts to scrape per loop
post_details = scrape_reddit_posts(subreddits, post_details, max_posts)

# Determine the most likely fake post of all scraped
print('begin classify\n')
is_fake_buffer = 0.92 # Must have greater than 92% confidence to be considered fake
chosen_post_index = find_fake_post(post_details, is_fake_buffer)

# Search Google for relevant articles to correct the post claim
print('begin search\n')
sources = serpapi_search(post_details[chosen_post_index]['title'])

# Summarize and extract source details
print('begin summarize\n')
summaries = []
for source in sources:
    summaries.append(summarize_article(source['url']))

# Build the model final response prompt
print('begin build prompt\n')
prompt = build_prompt(post_details[chosen_post_index]['title'], post_details[chosen_post_index]['body_text'], summaries)

# Send prompt to Hugging Face Inference API and generate a response
print('begin generate reply\n')
post_reply = generate_reply(prompt)

# Reply to the post with a detailed and cited correction
print('begin comment\n')
reply(post_details, chosen_post_index, post_reply)

# Save reply details in external database
print('begin db store\n')
success = save_reply(post_details['subreddit'],
                     post_details['id'],
                     post_details['title'],
                     post_details['body_text'],
                     post_reply,
                     sources,
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
