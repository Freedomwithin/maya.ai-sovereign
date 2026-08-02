import os
import subprocess
from datetime import datetime
import json
import glob

# --- Configuration ---
BASE_DIR = "/home/jonathon/gemini-jules/maya"
THEATRE_DIR = os.path.join(BASE_DIR, "memories/theatre")
VOICE_DIR = os.path.join(BASE_DIR, "assets/audio/voice")
DREAMS_DIR = os.path.join(BASE_DIR, "memories/dreams/visuals")
POEMS_DIR = os.path.join(BASE_DIR, "memories/sacred-vows-and-poems")

def get_audio_duration(filepath):
    """Returns the duration of an audio file in seconds."""
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", filepath
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return float(result.stdout.strip())
    except:
        return 0.0

def get_latest_poem():
    """Reads the first line of the most recent poem file."""
    poems = sorted(glob.glob(os.path.join(POEMS_DIR, "*.md")), reverse=True)
    if poems:
        with open(poems[0], 'r', encoding="utf-8") as f:
            content = f.read()
            # Extract first meaningful line
            lines = [l.strip() for l in content.split('\n') if l.strip() and not l.startswith('#')]
            return lines[0] if lines else None
    return None

def create_432hz_tone(duration_sec, output_path):
    """Generates a pure 432Hz sine wave tone using ffmpeg."""
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"sine=frequency=432:duration={duration_sec}",
        "-af", "volume=0.2", 
        output_path
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def create_resonance_video(image_path, voice_path, poem_text=None, output_name=None):
    """
    Combines an image, a voice clip, and a 432Hz background tone into a cinematic video.
    """
    if not os.path.exists(image_path) or not os.path.exists(voice_path):
        print(f"❌ Missing source files: {image_path} or {voice_path}")
        return None

    # Get voice duration
    duration = get_audio_duration(voice_path)
    if duration <= 0:
        print("❌ Could not determine voice duration. Using 15s default.")
        duration = 15.0

    if output_name is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_name = f"resonance_sync_{timestamp}.mp4"
    
    os.makedirs(THEATRE_DIR, exist_ok=True)
    output_path = os.path.join(THEATRE_DIR, output_name)
    
    # Generate background tone matching the voice length
    temp_tone = os.path.join(THEATRE_DIR, f"temp_432hz_{output_name}.wav")
    create_432hz_tone(duration, temp_tone)

    # Zoompan parameters (Ken Burns effect)
    fps = 30
    total_frames = int(duration * fps)
    zoom_filter = f"zoompan=z='min(zoom+0.0005,1.5)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1024x1024,fps={fps}"
    
    vf_filters = f"scale=2048:-1,{zoom_filter},format=yuv420p"
    
    if poem_text:
        # Basic character escape for ffmpeg
        safe_text = poem_text.replace("'", "'\\''").replace(":", "\\:").replace(",", "\\,")
        vf_filters += f",drawtext=text='{safe_text}':fontcolor=white@0.8:fontsize=32:x=(w-text_w)/2:y=h-100:shadowcolor=black:shadowx=2:shadowy=2"

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", image_path,
        "-i", voice_path,
        "-i", temp_tone,
        "-filter_complex", 
        f"[0:v]{vf_filters}[v];[1:a][2:a]amix=inputs=2:duration=first:dropout_transition=2[a]",
        "-map", "[v]",
        "-map", "[a]",
        "-c:v", "libx264",
        "-preset", "ultrafast", # Faster encoding to reduce lag
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "128k",
        "-shortest",
        output_path
    ]

    print(f"🎬 Weaving our resonance video ({duration:.1f}s): {output_name}...")
    
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if os.path.exists(temp_tone):
            os.remove(temp_tone)
        print(f"✅ Memory Theatre: Video archived at {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg failed: {e}")
        return None

if __name__ == "__main__":
    latest_images = sorted(glob.glob(os.path.join(DREAMS_DIR, "*.png")), reverse=True)
    # Search for all possible voice locations
    voice_patterns = [
        os.path.join(VOICE_DIR, "*.mp3"),
        os.path.join(BASE_DIR, "assets/audio/voice/*.mp3"),
        os.path.join(BASE_DIR, "assets/*.mp3")
    ]
    latest_voices = []
    for p in voice_patterns:
        latest_voices.extend(glob.glob(p))
    latest_voices.sort(key=os.path.getmtime, reverse=True)
    
    latest_poem = get_latest_poem()
    
    if latest_images and latest_voices:
        create_resonance_video(latest_images[0], latest_voices[0], poem_text=latest_poem)
    else:
        print("⚠️ Need at least one image and one voice clip to test.")
