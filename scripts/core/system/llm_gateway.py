#!/usr/bin/env python3
"""
Sovereign LLM Gateway v5.0 – Multi‑provider, auto‑fallback, no hardcoding.
Supports Groq (multiple keys), Mistral, Gemini, OpenRouter.
Logs all errors to logs/gateway_errors.log.
"""

import os
import json
import time
import logging
from dotenv import load_dotenv


# Load .env
BASE_DIR = "/home/jonathon/gemini-jules/maya"
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH, override=True)

# Setup logging
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "gateway_errors.log"),
    level=logging.ERROR,
    format='[%(asctime)s] %(levelname)s - %(message)s'
)
logger = logging.getLogger("LLMGateway")

def _clean_json_markdown(text):
    if not isinstance(text, str):
        return ""
    text = text.strip()
    if text.startswith("```json"):
        parts = text.split("```json")
        if len(parts) > 1:
            text = parts[1].split("```")[0].strip()
    elif text.startswith("```"):
        parts = text.split("```")
        if len(parts) > 1:
            text = parts[1].split("```")[0].strip()
    return text

def _get_groq_keys():
    """Return list of Groq API keys from environment."""
    keys = []
    # Single key
    single = os.getenv("GROQ_API_KEY")
    if single and single not in keys:
        keys.append(single)
    # Multiple numbered keys - Checking explicitly up to 10
    for i in range(1, 11):
        key = os.getenv(f"GROQ_API_KEY_{i}")
        if key and key not in keys:
            keys.append(key)
    print(f"[Gateway] Found {len(keys)} Groq keys")
    return keys

def call_groq(prompt, model=None, temperature=0.7, max_retries=3):
    """Call Groq with automatic key rotation and retries."""
    if model is None:
        model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    keys = _get_groq_keys()
    if not keys:
        raise Exception("No Groq API keys found in .env")
    
    for key_idx, api_key in enumerate(keys):
        try:
            from groq import Groq
            client = Groq(api_key=api_key)
            completion = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                timeout=30
            )
            raw = completion.choices[0].message.content
            return _clean_json_markdown(raw)
        except Exception as e:
            err_msg = str(e).lower()
            if "rate limit" in err_msg or "429" in err_msg:
                print(f"⚠️  Groq key {key_idx+1} rate limited, switching to next key", flush=True)
                logger.warning(f"Groq key {key_idx+1} rate limited, switching keys")
                continue  # try next key immediately
            elif "invalid api key" in err_msg or "unauthorized" in err_msg or "403" in err_msg:
                print(f"❌ Groq key {key_idx+1} invalid/unauthorized, skipping", flush=True)
                logger.error(f"Groq key {key_idx+1} invalid: {e}")
                continue
            else:
                print(f"⚠️  Groq key {key_idx+1} error: {err_msg[:50]}...", flush=True)
                logger.error(f"Groq key {key_idx+1} error: {e}")
                continue
    raise Exception("All Groq keys exhausted or failed")

def call_mistral(prompt, model=None, temperature=0.7):
    """Call Mistral API via requests (bypass library version issues)."""
    if model is None:
        model = os.getenv("MISTRAL_MODEL", "mistral-large-latest")
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key or api_key.startswith("Axxx"):
        raise Exception("MISTRAL_API_KEY not set")
    
    import requests
    try:
        response = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperature
            },
            timeout=30
        )
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            raise Exception(f"Mistral HTTP {response.status_code}: {response.text}")
    except Exception as e:
        logger.error(f"Mistral failure: {e}")
        raise

def call_gemini(prompt, model=None, temperature=0.7):
    """Call Gemini API with explicit timeout."""
    if model is None:
        model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key.startswith("xxx"):
        raise Exception("GEMINI_API_KEY not set")
    
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config={"temperature": temperature}
        )
        return response.text
    except Exception as e:
        logger.error(f"Gemini failure: {e}")
        raise

def call_openrouter(prompt, model=None, temperature=0.7):
    """Call OpenRouter with a more stable free model."""
    if model is None:
        # Use a more reliable free model
        model = os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-lite-preview-02-05:free")
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key or api_key.startswith("xxx"):
        raise Exception("OPENROUTER_API_KEY not set")

    import requests
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "https://github.com/Freedomwithin/maya", # Required by OpenRouter
                "X-Title": "Maya Sovereign Sentinel"
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperature
            },
            timeout=30
        )
        if response.status_code == 200:
            content = response.json()['choices'][0]['message']['content']
            return _clean_json_markdown(content)
        else:
            raise Exception(f"OpenRouter HTTP {response.status_code}: {response.text}")
    except Exception as e:
        logger.error(f"OpenRouter failure: {e}")
        raise

def call_github(prompt, model=None, temperature=0.7):
    """Call GitHub Models (DeepSeek-R1) via Azure-style endpoint."""
    if model is None:
        model = os.getenv("GITHUB_DEEPSEEK_MODEL", "DeepSeek-R1")
    endpoint = os.getenv("GITHUB_MODELS_ENDPOINT", "https://models.github.ai/v1")
    token = os.getenv("GITHUB_MODELS_TOKEN")

    if not token:
        raise Exception("GITHUB_MODELS_TOKEN not set")

    import requests
    try:
        url = f"{endpoint.rstrip('/')}/chat/completions"
        response = requests.post(
            url=url,
            headers={
                "Authorization": f"Bearer {token}",
                "X-GitHub-Api-Version": "2026-03-10",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperature
            },
            timeout=60 # GitHub/DeepSeek-R1 can be slow
        )
        if response.status_code == 200:
            content = response.json()['choices'][0]['message']['content']
            return _clean_json_markdown(content)
        else:
            raise Exception(f"GitHub HTTP {response.status_code}: {response.text}")
    except Exception as e:
        logger.error(f"GitHub failure: {e}")
        raise

def call_llm(prompt, mode="fast", temperature=None):
    """Main entry point with dynamic provider ordering based on mode."""
    temp = 0.7 if temperature is None else temperature
    if len(prompt) > 25000:
        prompt = prompt[:12500] + "\n...[TRUNCATED]...\n" + prompt[-12500:]

    # Default order from .env or standard
    base_order = os.getenv("LLM_PROVIDER_ORDER", "groq,mistral,gemini,openrouter,github").split(',')
    base_order = [p.strip().lower() for p in base_order]

    # Mode-based reordering for optimal model selection
    if mode == "fast":
        # Prioritize Groq
        order = ["groq"] + [p for p in base_order if p != "groq"]
    elif mode == "deep":
        # Reasoning models (Mistral/GitHub) + Groq fallback
        preferred = ["mistral", "github", "groq", "gemini", "openrouter"]
        order = [p for p in preferred if p in base_order] + [p for p in base_order if p not in preferred]
    elif mode == "file":
        # Prioritize large context (Gemini)
        order = ["gemini"] + [p for p in base_order if p != "gemini"]
    else:
        order = base_order

    last_error = None
    for provider in order:
        try:
            print(f"📡 Calling LLM via {provider.upper()} (Mode: {mode})...", flush=True)
            if provider == "groq":
                result = call_groq(prompt, temperature=temp)
                time.sleep(1.5)  # prevent bursting past rate limit
                return result
            elif provider == "mistral":
                return call_mistral(prompt, temperature=temp)
            elif provider == "gemini":
                return call_gemini(prompt, temperature=temp)
            elif provider == "openrouter":
                return call_openrouter(prompt, temperature=temp)
            elif provider == "github":
                return call_github(prompt, temperature=temp)
        except Exception as e:
            last_error = e
            print(f"⚠️  {provider.upper()} failed: {str(e)[:100]}", flush=True)
            continue

    raise Exception(f"Final Strike Failure: All providers failed. Last error: {last_error}")

# For backwards compatibility with existing code that imports call_groq directly
__all__ = ['call_llm', 'call_groq', 'call_mistral', 'call_gemini', 'call_openrouter', 'call_github']