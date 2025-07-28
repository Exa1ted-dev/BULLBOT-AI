import time
import threading
from flask import Flask
from reddit_bot import reddit, scrape_reddit_posts, find_fake_post, summarize_article, build_prompt, reply
from ai_services import generate_reply, serpapi_search
from database_handler import save_reply

app = Flask(__name__)

@app.route('/')
def home():
    return "BULLBOT is running!"

def run_bot():
    try:
        print('Running new bot cycle...\n')

        # Scrape some new Reddit posts
        print('begin scrape\n')
        subreddits = reddit.subreddit("conspiracy+conspiracy_commons+antiVaxxers+COVID19_conspiracy+alternativehealth+WallStreetBets+FlatEarth+woo+NoNewNormal+China_Flu+TheRedPill+MGTOW") # Subreddits to scrape posts from
        post_details = [] # List of posts scraped
        max_posts = 5 # How many posts to scrape per loop
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
        summaries = [summary for source in sources if (summary := summarize_article(source['url'])) is not None]

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
        success = save_reply(post_details[chosen_post_index]['subreddit'],
                            post_details[chosen_post_index]['id'],
                            post_details[chosen_post_index]['title'],
                            post_details[chosen_post_index]['body_text'],
                            post_reply,
                            sources,
                            )


        print("Reply saved to Supabase successfully!" if success else "Reply already exists or failed to save.")
    except Exception as e:
        print(f"Error in bot: {e}")

def main():
    sleep_in_mins = 60

    def bot_loop():
        while True:
            try:
                run_bot()
            except Exception as e:
                print(f"Error in bot: {e}")
            time.sleep(sleep_in_mins * 60)

    # Start bot loop in background
    threading.Thread(target=bot_loop, daemon=True).start()
    # Dummy web server to keep Render web service running
    app.run(host='0.0.0.0', port=10000)

if __name__ == '__main__':
    main()

# Change server type
