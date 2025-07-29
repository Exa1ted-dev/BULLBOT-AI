import requests

url = "https://eppbwrtvihnxjtwooyzn.supabase.co/rest/v1/replies"

headers = {
    "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVwcGJ3cnR2aWhueGp0d29veXpuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTM0ODA4MDksImV4cCI6MjA2OTA1NjgwOX0.e6NeK5pl3cCsILxvhSBSH2XhCyEqPzUshQihmDPX9mo",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVwcGJ3cnR2aWhueGp0d29veXpuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTM0ODA4MDksImV4cCI6MjA2OTA1NjgwOX0.e6NeK5pl3cCsILxvhSBSH2XhCyEqPzUshQihmDPX9mo",
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()

    for entry in data:
        log = f"""
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
ID
---------------------------------------------------------

{entry['id']}

---------------------------------------------------------
Subreddit
---------------------------------------------------------

{entry['subreddit']}

---------------------------------------------------------
Original Reddit Post ID
---------------------------------------------------------

{entry['reddit_post_id']}

---------------------------------------------------------
Original Reddit Post Title
---------------------------------------------------------

{entry['reddit_post_title']}

---------------------------------------------------------
Original Reddit Post Body
---------------------------------------------------------

{entry['reddit_post_body']}

---------------------------------------------------------
BULLBOT Generated Reply
---------------------------------------------------------

{entry['reply_text']}

---------------------------------------------------------
Source Urls
---------------------------------------------------------

{entry['source_urls']}

---------------------------------------------------------
Created At
---------------------------------------------------------

{entry['created_at']}





"""
        with open('logs.txt', 'a') as file:
            file.write(log)
