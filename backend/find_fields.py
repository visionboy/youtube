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

print("=== All Keys ===")
print(list(video.keys()))

print("\n=== Looking for statistics ===")
for key in video.keys():
    if 'count' in key.lower() or 'stat' in key.lower() or 'play' in key.lower() or 'like' in key.lower() or 'comment' in key.lower() or 'share' in key.lower():
        print(f"{key}: {video[key]}")

print("\n=== Looking for cover/thumbnail ===")
for key in video.keys():
    if 'cover' in key.lower() or 'thumb' in key.lower() or 'image' in key.lower():
        print(f"{key}: {video[key]}")

print("\n=== Author info ===")
author = video.get('author', {})
if author:
    print(f"Author keys: {list(author.keys())}")
    for key in author.keys():
        if 'follower' in key.lower() or 'count' in key.lower():
            print(f"  {key}: {author[key]}")
