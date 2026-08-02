import os
import requests

def call_mistral(prompt):
    api_key = "SmIH402KY5KcCVFvLeecFzEou1XbNYQd"
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistral-small-latest",
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        return response.status_code, response.text
    except Exception as e:
        return None, str(e)

print(call_mistral("hello"))
