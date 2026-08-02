import urllib.request
import json

apikey = "4i89OB0sd8GrLyeJfBdrUDuABpe3q469"
url = "https://api.rootdata.com/open/get_fac"

payload = {
    "page": 1,
    "page_size": 10,
    "start_time": "2026-02"
}

data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={
    'apikey': apikey,
    'language': 'en',
    'Content-Type': 'application/json'
})

try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode())
        if result.get('code') == 200:
            items = result.get('data', {}).get('items', [])
            print(json.dumps(items, indent=2))
        else:
            print(f"Error from API: {result}")
except Exception as e:
    print(f"Error fetching data: {e}")
