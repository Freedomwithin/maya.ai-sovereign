import urllib.request
import json

# DefiLlama is completely free and public, no API key required for their raises endpoint!
# This is a much better first step than burning RootData credits.

url = "https://api.llama.fi/raises"
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        
        # Get the 20 most recent raises
        raises = data.get("raises", [])[:20]
        
        print("Latest 20 Crypto/Web3 Fundraises from DefiLlama:\n")
        for raise_data in raises:
            name = raise_data.get('name', 'Unknown')
            round_type = raise_data.get('round', 'Unknown')
            amount = raise_data.get('amount', 0)
            sector = raise_data.get('sector', 'Unknown')
            date = raise_data.get('date', 'Unknown')
            source = raise_data.get('source', 'Unknown')
            
            # Convert timestamp to readable date if needed, or just print as is
            print(f"Project: {name}")
            print(f"Round: {round_type} - Amount: ${amount:,.2f}")
            print(f"Sector: {sector}")
            print(f"Source: {source}")
            print("-" * 40)
            
except Exception as e:
    print(f"Error fetching data: {e}")
