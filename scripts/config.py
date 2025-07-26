import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Reddit
CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
USER_AGENT = os.getenv('REDDIT_USER_AGENT')
USERNAME = os.getenv('REDDIT_USERNAME')
PASSWORD = os.getenv('REDDIT_PASSWORD')

# Tavily
TAVILY_API_KEY  = os.getenv('Tavily_API_KEY')

# Hugging Face
HF_API_KEY = os.getenv('HF_API_KEY')

# Supabase
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
