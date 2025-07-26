import requests
import config

# Load environment variables
TAVILY_API_KEY  = config.TAVILY_API_KEY
SERPAPI_KEY = config.SERPAPI_KEY
HF_API_KEY = config.HF_API_KEY

# Access Hugging Face Spaces classification model to determine whether a post is likely true or false
def classify_post_truth(post_title, post_body):
    hf_classify_url = 'https://Exa1ted-dev-BULLBOT-Post-Classification.hf.space/predict'
    full_text = f'Title: {post_title}\n\nBody: {post_body}'
    payload = {'text': full_text}

    try:
        response = requests.post(hf_classify_url, json=payload)
        response.raise_for_status() # Raise error if not status 200
        result = response.json()
        return result # {'label': 'LABEL_0', 'confidence': 0.968}
    except requests.RequestException as e:
        print(f'Error during post classification request: {e}')
        return None

# Search google for current, relevant sources to base responses on with SerpAPI
def serpapi_search(query):
    params = {
        'q': query,
        "api_key": SERPAPI_KEY,
        "engine": "google",
        "num": 3,
        "hl": "en"
    }

    response = requests.get("https://serpapi.com/search", params=params)
    data = response.json()

    results = data.get("organic_results", [])

    return [
        {
            "title": r.get("title"),
            "url": r.get("link"),
            "snippet": r.get("snippet", "")
        }
        for r in results
    ]

# Generate a final, informed post reply
def generate_reply(chosen_post_index, post_details, articles):
    debunk_payload = {
        'post_title': post_details[chosen_post_index]['title'],
        'post_body': post_details[chosen_post_index]['body_text'],
        'articles': articles
    }
    
    response = requests.post('https://Exa1ted-dev-BULLBOT-Response-Generation.hf.space/predict', json=debunk_payload)

    # Check if request was successful and content exists
    if response.status_code == 200 and response.text.strip():
        try:
            return response.json()
        except ValueError:
            print("❌ Failed to parse JSON. Response text:")
            print(response.text)
            return {"response": "Invalid JSON from model."}
    else:
        print(f"❌ Request failed with status {response.status_code}")
        print("Response text:", response.text)
        return {"response": f"Request failed or empty response: {response.status_code}"}
