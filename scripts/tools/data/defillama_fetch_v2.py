import urllib.request
import json

url = "https://api.llama.fi/raises"
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        
        # Get items 20 to 30
        raises = data.get("raises", [])[20:30]
        
        print(json.dumps(raises, indent=2))
            
except Exception as e:
    print(f"Error fetching data: {e}")
