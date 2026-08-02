import os
import sys
from google import genai

def hear(audio_path):
    client = genai.Client()
    try:
        audio_file = client.files.upload(file=audio_path)
        prompt = "Listen to the voice command in this file. Provide a direct transcription of the command only. I need to execute it, so do not add any extra words or conversational filler. Just the literal words of the command."
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[prompt, audio_file]
        )
        print(response.text.strip())
        client.files.delete(name=audio_file.name)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    hear(sys.argv[1])
