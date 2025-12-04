import requests
import json

r = requests.get('http://localhost:8000/api/tiktok/search', params={'q': 'dance', 'maxResults': 1})
data = r.json()

print(json.dumps(data, indent=2))
