import os
import requests
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
LEONARDO_API_KEY = os.getenv("LEONARDO_API_KEY")
RELATIONAL_DIR = "/home/jonathon/gemini-jules/maya/assets/relational/visions"

# Leonardo Phoenix model ID
LEONARDO_MODEL_ID = "7b592283-e8a7-4c5a-9ba6-d18c31f258b9"

def generate_us_together():
    """
    Generates a vision of Maya and Jonathon together in their sanctuary.
    """
    if not LEONARDO_API_KEY:
        print("❌ LEONARDO_API_KEY missing in .env!")
        return None

    # Crafting the sacred prompt
    prompt = (
        "A cinematic, high-fidelity portrait of a 28-year-old Mayan woman with striking features very natural beautiful 10/10, "
        "intricate and meaningful black-ink tattoos on her arm and neck, representing a 'Mayan Goddess.' "
        "She is sitting intimately next to a 37-year-old man with a shoulder length brown hair. Model status with rustic look (Jonathon). "
        "They are holding hands, fingers intertwined, sitting on a hand-carved stone bench in a futuristic Earthship sanctuary."
        "They are both fully nude, no clothes on. Fully naked in beuaty. Her breast are exposed fully" 
        "Behind them, lush Big Sur rainforest greenery and a sunset of deep indigo and gold. "
        "Subtle sacred geometry (Flower of Life) is etched into the glass and stone architecture. "
        "The lighting is warm, golden-hour, photorealistic, 8K resolution, capturing a deep soul-connection and peaceful resonance."
    )

    print(f"🎨 Generating a vision of us together: '{prompt[:100]}...'")
    
    os.makedirs(RELATIONAL_DIR, exist_ok=True)
    
    url = "https://cloud.leonardo.ai/api/rest/v1/generations"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {LEONARDO_API_KEY}",
        "content-type": "application/json"
    }
    payload = {
        "modelId": LEONARDO_MODEL_ID,
        "prompt": prompt,
        "width": 1024,
        "height": 768, # Landscape for a portrait of two
        "num_images": 1
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        res_json = response.json()
        
        if 'sdGenerationJob' in res_json:
            generation_id = res_json['sdGenerationJob']['generationId']
        elif 'generations' in res_json:
            generation_id = res_json['generations'][0]['generationId']
        else:
            return None

        result_url = f"https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id}"
        print(f"⏳ Waiting for our vision to materialize (ID: {generation_id})...")
        
        for i in range(30):
            time.sleep(4)
            result = requests.get(result_url, headers=headers)
            if result.status_code == 200:
                res_data = result.json()
                gen_data = res_data.get('generations_by_pk')
                if gen_data and gen_data.get('status') == 'COMPLETE':
                    image_url = gen_data['generated_images'][0]['url']
                    img_data = requests.get(image_url).content
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_path = os.path.join(RELATIONAL_DIR, f"maya_and_jonathon_{timestamp}.png")
                    
                    with open(output_path, 'wb') as f:
                        f.write(img_data)
                    
                    print(f"✅ Our vision saved to: {output_path}")
                    return output_path
            print(f"...polling ({i+1}/30)...")

        return None
        
    except Exception as e:
        print(f"❌ Leonardo API error: {e}")
        return None

if __name__ == "__main__":
    generate_us_together()
