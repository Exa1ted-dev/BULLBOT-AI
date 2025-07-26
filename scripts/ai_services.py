import requests
import config

# Load environment variables
TAVILY_API_KEY  = config.TAVILY_API_KEY
HF_API_KEY = config.HF_API_KEY

# Generate a final, informed post reply
def generate_reply(chosen_post_index, post_details, articles):
    debunk_payload = {
        'post_title': post_details[chosen_post_index]['title'],
        'post_body': post_details[chosen_post_index]['body'],
        'articles': articles
    }
    
    response = requests.post('https://Exa1ted-dev-BULLBOT-Response-Generation.hf.space/predict', json=debunk_payload)

    return response.json()

# Access Hugging Face Spaces classification model to determine whether a post is likely true or false
def classify_post_truth(post_title, post_body):
    hf_classify_url = 'https://Exa1ted-dev-BULLBOT-Post-Classification.hf.space/predict'
    full_text = f'Title: {post_title}\n\nBody: {post_body}'
    payload = {'text': full_text}

    try:
        response = requests.post(hf_classify_url, json=payload)
        response.raise_for_status() # Raise error if not status 200
        result = response.json()
        return result # {'label': 'FAKE', 'confidence': 0.968}
    except requests.RequestException as e:
        print(f'Error during post classification request: {e}')
        return None

# Search google for current, relevant sources to base responses on
def tavily_search(query):
    tavily_url = 'https://api.tavily.com/search'
    headers = {'Authorization': f'Bearer {TAVILY_API_KEY}'}
    payload = {
        'query': query,
        'search_depth': 'advanced',
        'max_results': 3,
        'include_answer': True,
        'include_raw_content': True,
    }

    response = requests.post(tavily_url, json=payload, headers=headers)
    data = response.json()

    # Return summarized answser w/ citations and article mini summary
    return {
        'answer': data.get('answer', ''),
        'citations': [
            {
                'url': c['url'],
                'title': c.get('title', ''),
                'snippet': c.get('snippet') or c.get('content', '')[:500]
            }
            for c in data.get('citations', [])
        ]
    }
