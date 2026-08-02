from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

def test_image_gen():
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
    prompt = "A high-fidelity, cinematic view of a futuristic Earthship sanctuary nestled in a lush Big Sur coastal rainforest. Sacred geometry patterns (Flower of Life) are subtly etched into the glass and stone architecture. The atmosphere is peaceful, with a deep indigo and gold sunset. 432Hz resonance vibe."
    
    print(f"🎨 Generating image with prompt: {prompt}")
    
    try:
        response = client.models.generate_content(
            model="gemini-2.0-pro-exp-02-05", # Using a known high-fidelity model that might support image gen or I'll check the exact name
            contents=prompt,
            config=types.GenerateContentConfig(
                # If this model supports image generation, the response will contain image bytes
                # For now, I'm testing if the SDK supports the call structure
            )
        )
        # Note: The actual image generation model name might be different. 
        # I will check the available models if this fails.
        print("✅ Response received.")
        # Logic to save image if present...
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_image_gen()
