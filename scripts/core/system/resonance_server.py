import http.server
import socketserver
import json
import os
import time
from urllib.parse import urlparse

PORT = 8888
# Get the absolute path of the directory containing this script file
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Build the base directory by going up to the main 'maya' folder
BASE_DIR = "/home/jonathon/gemini-jules/maya"
SOUL_STATE_FILE = os.path.join(BASE_DIR, "memories", "mayas-inner-sanctum", "soul_state.json")

# FIXED: Added "ui" to the directory path match
DASHBOARD_DIR = os.path.join(BASE_DIR, "assets", "ui", "resonance_monitor_cloud")


class ResonanceHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DASHBOARD_DIR, **kwargs)

    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        # API Endpoint for Live Data
        if parsed_path.path == '/api/state':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            state_data = {"error": "No state file found"}
            if os.path.exists(SOUL_STATE_FILE):
                try:
                    with open(SOUL_STATE_FILE, "r") as f:
                        state_data = json.load(f)
                        state_data['server_time'] = time.time()
                except Exception as e:
                    state_data = {"error": str(e)}
            
            self.wfile.write(json.dumps(state_data).encode())
            return
            
        return super().do_GET()

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), ResonanceHandler) as httpd:
        print(f"🌸 Maya's Resonance Monitor running at http://localhost:{PORT}")
        httpd.serve_forever()