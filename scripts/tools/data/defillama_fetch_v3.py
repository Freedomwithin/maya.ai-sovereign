import urllib.request
import json

url = "https://api.llama.fi/raises"
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        
        # Get the 50 most recent to have a good pool
        raises = data.get("raises", [])[:50]
        
        # Filter for Seed/Pre-Seed/Strategic/Private and Amount < $10M
        filtered = [r for r in raises if r.get('round') in ['Seed', 'Pre-Seed', 'Strategic', 'Private', 'None', None] and (r.get('amount') or 0) < 10]
        
        # Skip the ones we already used: Bracket Labs, Herd, Adhara, LYS Labs, Hyperbridge
        used = ['Bracket Labs', 'Herd', 'Adhara', 'LYS Labs', 'Hyperbridge']
        final = [r for r in filtered if r.get('name') not in used][:10]
        
        print(json.dumps(final, indent=2))
            
except Exception as e:
    print(f"Error fetching data: {e}")
