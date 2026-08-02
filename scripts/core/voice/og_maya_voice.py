#!/usr/bin/env python3
import asyncio
import edge_tts
import subprocess
import os
import sys
import re
import time
import shutil
import random
from datetime import datetime

# ========== CONFIGURATION ==========
TEMPLATES = {
    "Rosa_Goddess": {"voice": "en-PH-RosaNeural", "pitch": "-4Hz", "rate": "+10%"},
}
DEFAULT_TEMPLATE = "Rosa_Goddess"
BASE_DIR = "/home/jonathon/gemini-jules/maya"
CHAT_MP3_DIR = os.path.join(BASE_DIR, "assets", "voice")
IMAGE_DIR = os.path.join(BASE_DIR, "assets", "maya", "maya_new_images")
LOG_FILE = "/tmp/maya_voice.log"

# ========== LOGGING ==========
def log(msg):
    try:
        with open(LOG_FILE, "a") as f:
            f.write(f"{datetime.now().isoformat()}: {msg}\n")
    except:
        pass

# ========== IMAGE SELECTION ==========
def get_random_image():
    """Pick a random image from the maya_new_images directory."""
    try:
        if not os.path.exists(IMAGE_DIR):
            return None
        images = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
        if not images:
            return None
        return os.path.join(IMAGE_DIR, random.choice(images))
    except:
        return None

# ========== TEXT SANITIZATION ==========
def sanitize_text(text):
    """Remove unsupported characters, limit length, provide fallback."""
    if not text or not isinstance(text, str):
        return "I have nothing to say right now."
    # Remove anything that's not alphanumeric, spaces, punctuation, or basic symbols
    text = re.sub(r'[^\w\s.,!?\-:;()\']', '', text)
    text = text.replace('\n', ' ').replace('\r', ' ')
    text = re.sub(r'\s+', ' ', text).strip()
    if len(text) > 500:
        text = text[:497] + "..."
    if not text:
        text = "I'm here, my love."
    return text

# ========== AUDIO PLAYBACK (WITH VISUAL PORTAL) ==========
def play_audio(filepath):
    """Play audio using mpv with visual portal injection."""
    try:
        mpv_path = shutil.which("mpv")
        if not mpv_path:
            log("❌ mpv not found. Install mpv or provide full path.")
            return False
        
        image_path = get_random_image()
        
        if image_path:
            # Visual Portal: Image as primary, Audio as external
            # --ontop: keep window on top
            # --no-border: no window decorations
            # --geometry: size and position (bottom-right)
            # --image-display-duration=inf: keep image visible while audio plays
            # We use subprocess.Popen and then wait for a bit to ensure it doesn't hang forever
            cmd = [
                mpv_path,
                "--ontop",
                "--no-border",
                "--geometry=450x450-20-20", 
                "--title=MAYA_VISUAL_PORTAL",
                "--image-display-duration=inf",
                f"--audio-file={filepath}",
                image_path
            ]
            log(f"🔊 Playing with Visual Portal: {filepath} | Image: {image_path}")
        else:
            # Fallback to audio-only if no image found
            cmd = [mpv_path, "--no-video", "--volume=100", "--keep-open=no", filepath]
            log(f"🔊 Playing (Audio Only): {filepath}")
        
        # Start mpv. We use Popen and then a short sleep + terminate to ensure it closes
        # since --image-display-duration=inf will hang.
        # For a 5-10 second speech, a 15s window is usually safe.
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Simple wait logic: wait 15s or until proc ends (though inf won't end)
        # Better: Since we know it's a short speech, we can just let it run 
        # and it will be cleaned up by the next voice call or we can sleep.
        # For now, let's sleep 8s (average speech length) then terminate.
        time.sleep(8)
        proc.terminate()
        
        return True
    except Exception as e:
        log(f"❌ Playback error: {e}")
        return False

# ========== TTS GENERATION ==========
async def generate_speech(text, template_name=None):
    """Generate TTS audio and play it (synchronous within async)."""
    os.makedirs(CHAT_MP3_DIR, exist_ok=True)
    template = TEMPLATES.get(template_name, TEMPLATES[DEFAULT_TEMPLATE])
    
    # Create a unique filename with timestamp
    timestamp = int(time.time() * 1000)
    output_path = os.path.join(CHAT_MP3_DIR, f"maya_voice_{timestamp}.mp3")
    
    # Clean the text before TTS
    clean_text = sanitize_text(text)
    log(f"🗣️ Speaking: \"{clean_text}\"")
    
    try:
        communicate = edge_tts.Communicate(
            clean_text,
            template["voice"],
            pitch=template["pitch"],
            rate=template["rate"]
        )
        await communicate.save(output_path)
        log(f"✅ TTS saved to {output_path}")
        
        # Play audio (this will block for the duration of playback)
        success = play_audio(output_path)
        
        # Clean up old files (optional: keep last 10)
        cleanup_old_audio(CHAT_MP3_DIR, keep=10)
        
        return success
    except Exception as e:
        log(f"❌ TTS generation error: {e}")
        return False

def cleanup_old_audio(directory, keep=10):
    """Delete oldest mp3 files, keeping only the most recent 'keep'."""
    try:
        files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".mp3")]
        if len(files) > keep:
            files.sort(key=os.path.getmtime)
            for f in files[:-keep]:
                os.remove(f)
                log(f"🗑️ Cleaned up old audio: {f}")
    except Exception as e:
        log(f"⚠️ Cleanup error: {e}")

# ========== MAIN ENTRY ==========
if __name__ == "__main__":
    # Get text from command line argument, or use default
    raw_text = sys.argv[1] if len(sys.argv) > 1 else "I am here, my love."
    asyncio.run(generate_speech(raw_text))