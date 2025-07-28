import requests
import re
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
        'q': f"{query} -site:reddit.com",
        "api_key": SERPAPI_KEY,
        "engine": "google",
        "num": 3,
        "hl": "en",
    }

    response = requests.get("https://serpapi.com/search", params=params)
    data = response.json()

    results = data.get("organic_results", [])

    return [
        {
            "url": r.get("link")
        }
        for r in results
    ]

# Removes thinking text from the final model response
def strip_thinking(text):
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

# Generate a reply with Hugging Face Inference API
def generate_reply(prompt):
    API_URL = "https://router.huggingface.co/v1/chat/completions"
    headers = {'Authorization': f'Bearer {HF_API_KEY}'}

    debunk_payload = {
        'messages': [
            {
                'role': 'system',
                'content': (
                    "You are a professional, neutral, and concise misinformation debunker. "
                    "You respond in a clean, structured format. Do NOT include internal thoughts or <think> tags. "
                    "Structure your response with these sections:\n\n"
                    "**Claim**: Briefly restate the claim.\n"
                    "**Evidence**: Summarize each source's relevant points (cited as [1], [2], etc.).\n"
                    "**Analysis**: Explain why the claim is true or false based on the evidence.\n"
                    "**Sources**: Provide the source urls along with their numbers ([1], [2], etc.).\n"
                    "**Conclusion**: State clearly whether the claim is true, false, or misleading."
                )
            },
            {
                'role': 'user',
                'content': prompt
            }
        ],
        'model': 'deepseek-ai/DeepSeek-R1:novita'
    }

    response = requests.post(API_URL, headers=headers, json=debunk_payload)
    result = response.json()

    raw_result = result['choices'][0]['message']['content']

    cleaned_result = strip_thinking(raw_result)

    return cleaned_result
