import requests
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

print("=== Checking for missing fields ===")
print(f"\n1. Author follower count:")
author = video.get('author', {})
print(f"   Author keys: {list(author.keys())}")
for key in author.keys():
    if 'follower' in key.lower() or 'fan' in key.lower():
        print(f"   {key}: {author[key]}")

print(f"\n2. Tags/Hashtags:")
for key in video.keys():
    if 'tag' in key.lower() or 'hash' in key.lower() or 'challenge' in key.lower():
        print(f"   {key}: {video[key]}")

print(f"\n3. Video IDs for embedding:")
print(f"   aweme_id: {video.get('aweme_id')}")
print(f"   video_id: {video.get('video_id')}")
print(f"   id: {video.get('id')}")

print(f"\n4. Video URL fields:")
for key in video.keys():
    if 'url' in key.lower() or 'play' in key.lower() or 'download' in key.lower():
        val = video[key]
        if isinstance(val, str) and len(val) < 100:
            print(f"   {key}: {val}")
