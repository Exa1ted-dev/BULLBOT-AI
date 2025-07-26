from supabase import create_client, Client
from datetime import datetime, timezone
import config

# Load environment variables
SUPABASE_URL = config.SUPABASE_URL
SUPABASE_KEY = config.SUPABASE_KEY

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_reply(subreddit: str, reddit_post_id: str, reddit_post_title: str, reply_text: str) -> bool:
    # Check if reply exists to avoid duplicates
    existing = supabase.table('replies').select('*').eq('reddit_post_id', reddit_post_id).execute()
    if existing.data and len(existing.data) > 0:
        return False # Already saved reply
    
    # Insert new reply
    response = supabase.table('replies').insert({
        'subreddit': subreddit,
        'reddit_post_id': reddit_post_id,
        'reddit_post_title': reddit_post_title,
        'reply_text': reply_text,
        'created_at': datetime.now(timezone.utc).isoformat(),
    }).execute()

    if response.status_code == 201 or response.status_code == 200:
        return True
    else:
        return False