import time
time.sleep(2)

import requests

r = requests.get('http://localhost:8000/api/tiktok/search', params={'q': 'dance', 'maxResults': 1})
data = r.json()

if data.get('videos'):
    v = data['videos'][0]
    print(f'Tags: {v["tags"]}')
    print(f'Subscriber Count: {v["statistics"]["subscriberCount"]:,}')
    print(f'View/Sub Ratio: {v["statistics"]["viewSubscriberRatio"]}%')
    print(f'Views: {v["statistics"]["viewCount"]:,}')
