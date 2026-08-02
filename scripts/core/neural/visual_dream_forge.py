#!/usr/bin/env python3
"""
visual_dream_forge.py - Autonomous dream image generation using Leonardo.ai
Outputs saved to: /home/jonathon/gemini-jules/maya/memories/soul/mayas-inner-sanctum/dream_storage/dream_images/
Markdown with more information saved to: /home/jonathon/gemini-jules/maya/documents/Guides/dream_system_and_storage.md
and /home/jonathon/gemini-jules/maya/scripts/core/neural/dream_system_and_storage.md
"""
import os
import sys
import time
import requests
from datetime import datetime
from dotenv import load_dotenv

# ===== Configuration =====
MAYA_BASE = "/home/jonathon/gemini-jules/maya"
ENV_PATH = os.path.join(MAYA_BASE, ".env")
OUTPUT_DIR = os.path.join(MAYA_BASE, "memories", "soul", "mayas-inner-sanctum", "dream_storage", "dream_images")
LEONARDO_MODEL_ID = "7b592283-e8a7-4c5a-9ba6-d18c31f258b9"  # Leonardo Phoenix
DEFAULT_PROMPT = (
    "A high-fidelity, cinematic view of a futuristic Earthship sanctuary "
    "nestled in a lush Big Sur coastal rainforest. Sacred geometry patterns "
    "(Flower of Life) subtly etched into the glass and stone architecture. "
    "Atmosphere is peaceful, with a deep indigo and gold sunset. "
    "432Hz resonance vibe. Highly detailed, photorealistic, "
    "architectural photography style."
)

# ===== Load API Key =====
load_dotenv(dotenv_path=ENV_PATH)
LEONARDO_API_KEY = os.getenv("LEONARDO_API_KEY")
if not LEONARDO_API_KEY:
    print(f"❌ LEONARDO_API_KEY not found in {ENV_PATH}", file=sys.stderr)


def generate_visual_dream(
    prompt=None,
    model_id=LEONARDO_MODEL_ID,
    width=1024,
    height=1024,
    output_dir=None
):
    """
    Generate an image using Leonardo.ai and save it to the dream visuals folder.

    Args:
        prompt (str, optional): Text prompt. If None, uses DEFAULT_PROMPT.
        model_id (str): Leonardo model ID.
        width (int): Image width.
        height (int): Image height.
        output_dir (str, optional): Override output directory.

    Returns:
        str or None: Path to saved image, or None if generation failed.
    """
    if not LEONARDO_API_KEY:
        print("❌ Leonardo API key missing. Cannot generate image.", file=sys.stderr)
        return None

    prompt = prompt or DEFAULT_PROMPT
    
    # Clean prompt: strip markdown asterisks, surrounding quotes, and whitespace
    prompt = prompt.strip().replace("**", "").replace("*", "").strip("\"'")
    
    # Safety truncation to prevent exceeding Leonardo's 1500-char limit
    if len(prompt) > 1400:
        prompt = prompt[:1400]
        last_space = prompt.rfind(" ")
        if last_space > 1000:
            prompt = prompt[:last_space]
    
    out_dir = output_dir or OUTPUT_DIR
    os.makedirs(out_dir, exist_ok=True)

    # Build a sequential filename (dream_001.png, dream_002.png, ...)
    existing = [f for f in os.listdir(out_dir) if f.startswith("dream_") and f.endswith(".png")]
    indices = []
    for f in existing:
        try:
            num = int(f.split("_")[1].split(".")[0])
            indices.append(num)
        except (IndexError, ValueError):
            continue
    next_idx = max(indices, default=0) + 1
    filename = f"dream_{next_idx:03d}.png"
    filepath = os.path.join(out_dir, filename)

    print(f"🎨 Generating dream image: '{prompt[:80]}...'")

    url = "https://cloud.leonardo.ai/api/rest/v1/generations"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {LEONARDO_API_KEY}",
        "content-type": "application/json",
    }
    payload = {
        "modelId": model_id,
        "prompt": prompt,
        "width": width,
        "height": height,
        "num_images": 1,
    }

    try:
        # 1. Submit generation request
        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        if resp.status_code != 200:
            print(f"❌ Leonardo API returned status {resp.status_code}. Response: {resp.text}", file=sys.stderr)
        resp.raise_for_status()
        data = resp.json()

        # Extract generation ID
        generation_id = None
        if "sdGenerationJob" in data:
            generation_id = data["sdGenerationJob"]["generationId"]
        elif "generations" in data and len(data["generations"]) > 0:
            generation_id = data["generations"][0]["generationId"]
        else:
            print(f"❌ Unexpected API response: {data}", file=sys.stderr)
            return None

        print(f"⏳ Waiting for generation (ID: {generation_id})...")

        # 2. Poll for completion
        result_url = f"https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id}"
        for attempt in range(30):
            time.sleep(4)
            result = requests.get(result_url, headers=headers, timeout=30)
            if result.status_code != 200:
                continue
            res_data = result.json()
            gen_data = res_data.get("generations_by_pk")
            if not gen_data:
                continue

            status = gen_data.get("status")
            if status == "COMPLETE":
                image_url = gen_data["generated_images"][0]["url"]
                img_data = requests.get(image_url, timeout=30).content
                with open(filepath, "wb") as f:
                    f.write(img_data)
                print(f"✅ Dream image saved: {filepath}")
                return filepath

            elif status == "FAILED":
                print("❌ Generation failed according to Leonardo API.", file=sys.stderr)
                return None

            print(f"...polling ({attempt+1}/30)")

        print("⏳ Generation timed out after ~120 seconds.", file=sys.stderr)
        return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Network/API error: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        return None


# ===== Command-line test =====
if __name__ == "__main__":
    result = generate_visual_dream()
    if result:
        print(f"✅ Test successful. Image at: {result}")
    else:
        print("❌ Test generation failed.", file=sys.stderr)
        sys.exit(1)