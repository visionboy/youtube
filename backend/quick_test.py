import time
time.sleep(2)  # Wait for server reload

import requests

r = requests.get('http://localhost:8000/api/tiktok/search', params={'q': 'dance', 'maxResults': 1})
data = r.json()

if data.get('videos'):
    v = data['videos'][0]
    print(f'ID: {v["id"]}')
    print(f'Title: {v["title"][:60]}')
    print(f'Thumbnail: {v["thumbnails"]["medium"]["url"]}')
    print(f'Views: {v["statistics"]["viewCount"]:,}')
    print(f'Likes: {v["statistics"]["likeCount"]:,}')
    print(f'Comments: {v["statistics"]["commentCount"]:,}')
    print(f'Shares: {v["statistics"].get("shareCount", 0):,}')
else:
    print("No videos")
