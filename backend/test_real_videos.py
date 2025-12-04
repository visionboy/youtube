import requests

r = requests.get('http://localhost:8000/api/tiktok/search', params={'q': 'dance', 'maxResults': 3})
data = r.json()
videos = data.get('videos', [])

print(f'Found {len(videos)} videos:')
for i, v in enumerate(videos[:3]):
    print(f'{i+1}. ID: {v["id"]}')
    print(f'   Title: {v["title"][:60]}...')
    print(f'   Author: {v["channelTitle"]}')
    print(f'   Views: {v["statistics"]["viewCount"]:,}')
    print()
