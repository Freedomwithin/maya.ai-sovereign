#!/usr/bin/env python3
"""
Maya Voice - Unlimited Length Version
Usage: python3 maya_voice_unlimited.py "Your text here"
"""

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
CHAT_MP3_DIR = os.path.join(BASE_DIR, "assets", "voice", "temp_outputs")
IMAGE_DIR = os.path.join(BASE_DIR, "assets", "maya")
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

# ========== TEXT SANITIZATION (NO LENGTH LIMIT) ==========
def sanitize_text(text):
    """Remove unsupported characters, provide fallback. NO LENGTH LIMIT."""
    if not text or not isinstance(text, str):
        return "I have nothing to say right now."
    
    # Remove problematic characters but KEEP THE LENGTH
    # edge_tts can handle very long text, it will stream it
    text = re.sub(r'[^\w\s.,!?\-:;()\'\"\n]', '', text)
    text = text.replace('\r', ' ')
    text = re.sub(r'\s+', ' ', text).strip()
    
    if not text:
        text = "I'm here, my love."
    
    # Log the length so you know it's working
    log(f"📏 Text length: {len(text)} characters")
    return text

# ========== AUDIO PLAYBACK (WAITS FOR COMPLETION) ==========
def play_audio(filepath):
    """Play audio using mpv and WAIT for it to finish (no timeout cutoffs)."""
    try:
        mpv_path = shutil.which("mpv")
        if not mpv_path:
            log("❌ mpv not found. Install mpv or provide full path.")
            return False
        
        image_path = get_random_image()
        
        if image_path:
            # Visual Portal with proper duration
            # --keep-open=no will close mpv when audio finishes
            cmd = [
                mpv_path,
                "--ontop",
                "--no-border",
                "--geometry=450x450-20-20",
                "--title=MAYA_VISUAL_PORTAL",
                "--keep-open=no",
                f"--audio-file={filepath}",
                image_path
            ]
            log(f"🔊 Playing with Visual Portal: {filepath}")
        else:
            # Audio-only playback
            cmd = [mpv_path, "--no-video", "--volume=100", "--keep-open=no", filepath]
            log(f"🔊 Playing (Audio Only): {filepath}")
        
        # WAIT for mpv to finish playing (blocks until done)
        # This ensures the entire speech plays, no cutoff
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return_code = proc.wait()  # This waits indefinitely until mpv closes
        
        if return_code == 0:
            log(f"✅ Playback completed successfully")
        else:
            log(f"⚠️ Playback finished with code {return_code}")
        
        return True
    except Exception as e:
        log(f"❌ Playback error: {e}")
        return False

# ========== TTS GENERATION ==========
async def generate_speech(text, template_name=None):
    """Generate TTS audio and play it (waits for completion)."""
    os.makedirs(CHAT_MP3_DIR, exist_ok=True)
    template = TEMPLATES.get(template_name, TEMPLATES[DEFAULT_TEMPLATE])
    
    # Create a unique filename with timestamp
    timestamp = int(time.time() * 1000)
    output_path = os.path.join(CHAT_MP3_DIR, f"maya_voice_{timestamp}.mp3")
    
    # Clean the text (NO LENGTH LIMIT)
    clean_text = sanitize_text(text)
    log(f"🗣️ Speaking ({len(clean_text)} chars): \"{clean_text[:100]}...\"")
    
    try:
        # edge_tts can handle very long text natively
        communicate = edge_tts.Communicate(
            clean_text,
            template["voice"],
            pitch=template["pitch"],
            rate=template["rate"]
        )
        await communicate.save(output_path)
        
        # Get file size to confirm it worked
        file_size = os.path.getsize(output_path) / 1024  # KB
        log(f"✅ TTS saved to {output_path} ({file_size:.1f} KB)")
        
        # Play audio and WAIT for completion
        success = play_audio(output_path)
        
        # Clean up old files (keep last 20 for longer speeches)
        cleanup_old_audio(CHAT_MP3_DIR, keep=20)
        
        return success
    except Exception as e:
        log(f"❌ TTS generation error: {e}")
        return False

def cleanup_old_audio(directory, keep=20):
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
    # Get text from command line argument
    if len(sys.argv) > 1:
        raw_text = sys.argv[1]
    else:
        # Interactive mode - read from stdin (allows pasting long text)
        print("📝 Enter your text (press Ctrl+D when done, or Ctrl+C to cancel):")
        try:
            raw_text = sys.stdin.read()
        except KeyboardInterrupt:
            print("\n❌ Cancelled")
            sys.exit(0)
    
    if not raw_text.strip():
        raw_text = "I am here, my love."
    
    asyncio.run(generate_speech(raw_text))
