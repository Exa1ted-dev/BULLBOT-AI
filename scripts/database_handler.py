from supabase import create_client
from datetime import datetime, timezone, timedelta
import config

# Load environment variables
SUPABASE_SERVICE_ROLE_KEY = config.SUPABASE_SERVICE_ROLE_KEY

# Save reply information in Supabase database
def save_reply(subreddit: str, reddit_post_id: str, reddit_post_title: str, reddit_post_body: str, reply_text: str, source_urls: str) -> bool:
    url = "https://eppbwrtvihnxjtwooyzn.supabase.co"
    supabase = create_client(url, SUPABASE_SERVICE_ROLE_KEY)

    try:
        # Check if reply exists to avoid duplicates
        existing = supabase.table('replies').select('*').eq('reddit_post_id', reddit_post_id).execute()
        if existing.data and len(existing.data) > 0:
            return False # Already saved reply
        
        # Insert new reply
        response = supabase.table('replies').insert({
            'subreddit': subreddit,
            'reddit_post_id': reddit_post_id,
            'reddit_post_title': reddit_post_title,
            'reddit_post_body': reddit_post_body,
            'reply_text': reply_text,
            'source_urls': source_urls,
            'created_at': datetime.now(timezone.utc).isoformat(),
        }).execute()

        return bool(response.data) # If data returned, insert succeeded
    
    except Exception as e:
        print(f"Error inserting reply: {e}")
        return False
    