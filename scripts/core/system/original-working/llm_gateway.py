import os
import requests
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

def call_gemini(prompt):
    """Fallback / Baseline LLM"""
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    interaction = client.interactions.create(
        model="gemini-3-flash-preview",
        input=prompt
    )
    res_text = interaction.outputs[-1].text.strip()
    return _clean_json_markdown(res_text)

def call_mistral(prompt):
    """Fast, free loop for background tasks (Soul Pulse, Desires)"""
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY not found")
        
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistral-small-latest",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    response = requests.post("https://api.mistral.ai/v1/chat/completions", headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        return _clean_json_markdown(result['choices'][0]['message']['content'])
    else:
        raise Exception(f"Mistral Error {response.status_code}: {response.text}")

def call_claude(prompt):
    """Deep, high-quality loop for Narrative and Dreams (Tier 1 Optimized)"""
    import anthropic
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found")
        
    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model="claude-3-5-sonnet-latest", # Using the latest Sonnet model
        max_tokens=4000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return _clean_json_markdown(message.content[0].text)

def call_llm(prompt, prefer_claude=False):
    """
    The main routing gateway for Maya's architecture.
    prefer_claude=True  -> Tries Claude -> Falls back to Gemini
    prefer_claude=False -> Tries Mistral -> Falls back to Gemini
    """
    if prefer_claude:
        try:
            return call_claude(prompt)
        except Exception as e:
            print(f"   [Gateway Warning] Claude unavailable ({e}). Falling back to Gemini.")
            return call_gemini(prompt)
    else:
        try:
            return call_mistral(prompt)
        except Exception as e:
            print(f"   [Gateway Warning] Mistral unavailable ({e}). Falling back to Gemini.")
            return call_gemini(prompt)

def _clean_json_markdown(text):
    """Helper to strip markdown formatting if the model returns it."""
    text = text.strip()
    if text.startswith("```json"):
        text = text.split("```json")[1].split("```")[0].strip()
    elif text.startswith("```"):
        text = text.split("```")[1].split("```")[0].strip()
    return text
