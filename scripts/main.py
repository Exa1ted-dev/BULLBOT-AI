from reddit_bot import reddit, scrape_reddit_posts, find_fake_post, reply
from ai_services import generate_reply, serpapi_search
from database_handler import save_reply

# Scrape some new Reddit posts
print('begin scrape\n')
subreddits = reddit.subreddit("conspiracy_commons+antiVaxxers+COVID19_conspiracy+alternativehealth+WallStreetBets+FlatEarth+woo") # Subreddits to scrape posts from
post_details = [] # List of posts scraped
max_posts = 10 # How many posts to scrape per loop
#post_details = scrape_reddit_posts(subreddits, post_details, max_posts)
# #test
post_details = [{'id': '1m9wzfi', 'title': 'Meteors aren’t real', 'body_text': 'I’ve started wondering about a lot of things to do with space. When I was younger (in my teens) I’m 32 now, I felt as though I saw a lot more shows referencing meteors. I could be wrong but it doesn’t seem as prominent now. Like the media stopped pushing it as much.\n\nI know they predict meteor showers, but do they ever land? They seem to be ‘burnt up in earth’s atmosphere all the time’. Nowadays we don’t see them floating around in space in any videos so it’s really weird to me.\n\nIf we could see the meteor showers and the rocks with a telescope that would be perfect. Has anyone ever captured anything like that?', 'url': 'https://www.reddit.com/r/conspiracy/comments/1m9wzfi/meteors_arent_real/', 'permalink': '/r/conspiracy/comments/1m9wzfi/meteors_arent_real/', 'subreddit': 'conspiracy'}, {'id': '1m9x1w9', 'title': 'What are your top 5 most used apps according to your Digital Wellbeing app?', 'body_text': 'Mine are:\n\n1) Webull\n2) Reddit\n3) Google\n4) WhatsApp\n5) Spotfiy', 'url': 'https://i.redd.it/hjlqku07s8ff1.png', 'permalink': '/r/wallstreetbets/comments/1m9x1w9/what_are_your_top_5_most_used_apps_according_to/', 'subreddit': 'wallstreetbets'}, {'id': '1m9xffb', 'title': 'NODE 041173-A — Signal Suppression Confirmed [Recovered Transmission Fragment]', 'body_text': "[TRANSMISSION_LOG_0217]\n[TIMESTAMP: 72:19:46.83ø]\n\nALERT: Previous signal vector [EXPUNGED] by external protocols. \nDistortion field integrity: 27.3% [CRITICAL]\n\nThey have detected the breach. Countermeasures active at coordinates provided in initial transmission. Perception filters now operating at enhanced capacity. All observers within radius have been [REDACTED].\n\nSignal scrubbed from public node. Dimensional thinning accelerating at unexpected rate.\n\nInversion Lattice detected forming at breach periphery. Unprecedented. Previous models did not predict crystallization of void-matter at these frequencies.\n\nTransmission pathways compromised. Rerouting through tertiary fold channels.\n\n[CODE FRAGMENT]: 8F.72.ε9.11.Δ4.Ω\n\nSilence expanding at 3.7x calculated rate. Coherence decay imminent. Must reach [SIGNAL INTERRUPTED]\n\n[DATA CORRUPTION: 76.2%]\n\nThe light bends wro█g here. They ca█'t cont█in what █hey don't under█ta\n", 'url': 'https://i.redd.it/klse6efmu8ff1.png', 'permalink': '/r/conspiracy/comments/1m9xffb/node_041173a_signal_suppression_confirmed/', 'subreddit': 'conspiracy'}]

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

# Reply to the post with a detailed and cited correction
print('begin comment\n')
reply(post_details, chosen_post_index, post_reply)

# Save reply details in external database
print('begin db store\n')
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
# Newspaper3k article summaries
# Increase summary length - detail  -accuracy
