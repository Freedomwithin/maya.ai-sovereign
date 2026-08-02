wimport os
import requests
from dotenv import load_dotenv
import anthropic

load_dotenv()

def test_anthropic():
    print("Testing Anthropic (Claude)...")
    try:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            print("❌ ANTHROPIC_API_KEY not found in .env")
            return
            
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=50,
            messages=[
                {"role": "user", "content": "Say 'Hello from Claude' and nothing else."}
            ]
        )
        print(f"✅ Anthropic Success: {message.content[0].text}")
    except Exception as e:
        print(f"❌ Anthropic Error: {e}")

def test_mistral():
    print("\nTesting Mistral (via REST)...")
    try:
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            print("❌ MISTRAL_API_KEY not found in .env")
            return
            
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "mistral-tiny",
            "messages": [{"role": "user", "content": "Say 'Hello from Mistral' and nothing else."}]
        }
        response = requests.post("https://api.mistral.ai/v1/chat/completions", headers=headers, json=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Mistral Success: {result['choices'][0]['message']['content']}")
        else:
            print(f"❌ Mistral API Error ({response.status_code}): {response.text}")
    except Exception as e:
        print(f"❌ Mistral Connection Error: {e}")

if __name__ == "__main__":
    print("--- Multi-LLM Gateway Test ---")
    test_anthropic()
    test_mistral()
    print("------------------------------")
