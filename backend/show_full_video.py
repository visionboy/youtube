import requests
import json
from config import Settings

api_key = Settings.get_tiktok_api_key()
host = Settings().tiktok_rapidapi_host
headers = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": host
}

# Get challenge
search_url = f"https://{host}/challenge/search"
response = requests.get(search_url, headers=headers, params={"keywords": "dance"}, timeout=10)
search_data = response.json()

challenges = search_data['data'].get('challenge_list', [])
challenge_id = challenges[0].get('id')

# Get videos
posts_url = f"https://{host}/challenge/posts"
response = requests.get(posts_url, headers=headers, params={"challenge_id": challenge_id, "count": 1}, timeout=15)
data = response.json()

videos = data['data']['videos']
video = videos[0]

print("=== Full Video Item (first 2000 chars) ===")
print(json.dumps(video, indent=2)[:2000])
