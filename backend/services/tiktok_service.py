from typing import List, Dict, Optional
import random
import requests
from datetime import datetime, timedelta
from config import Settings

class TikTokService:
    def __init__(self):
        pass
    
    def search_videos(
        self,
        query: str,
        max_results: int = 25,
        order: str = "relevance",
        published_after: Optional[str] = None,
        video_duration: Optional[str] = None,
        min_ratio: Optional[float] = None,
        min_comments: Optional[int] = None,
        tag: Optional[str] = None,
        page_token: Optional[str] = None
    ) -> Dict:
        """
        Search for TikTok videos. Uses RapidAPI if key is configured, otherwise Mock.
        """
        api_key = Settings.get_tiktok_api_key()
        
        if api_key:
            return self._search_rapidapi(
                api_key, query, max_results, order, published_after, 
                video_duration, min_ratio, min_comments, tag, page_token
            )
            
        # Mock data generation (Fallback)
        videos = []
        for i in range(max_results):
            view_count = random.randint(1000, 1000000)
            like_count = int(view_count * random.uniform(0.05, 0.2))
            comment_count = int(view_count * random.uniform(0.001, 0.01))
            subscriber_count = random.randint(10000, 5000000)
            
            ratio = 0
            if subscriber_count > 0:
                ratio = (view_count / subscriber_count) * 100

            # Filter logic (mock)
            if min_ratio is not None and ratio < min_ratio:
                continue
            if min_comments is not None and comment_count < min_comments:
                continue

            video_data = {
                'id': f'tiktok_{random.randint(100000, 999999)}',
                'title': f'TikTok Video {i+1} - {query}',
                'description': f'This is a mock TikTok video description for {query}. #tiktok #viral',
                'channelTitle': f'TikTokUser_{random.randint(1000, 9999)}',
                'publishedAt': (datetime.utcnow() - timedelta(days=random.randint(0, 30))).isoformat("T") + "Z",
                'thumbnails': {
                    'default': {
                        'url': 'https://placehold.co/120x90?text=TikTok',
                        'width': 120,
                        'height': 90
                    },
                    'medium': {
                        'url': 'https://placehold.co/320x180?text=TikTok+Video',
                        'width': 320,
                        'height': 180
                    },
                    'high': {
                        'url': 'https://placehold.co/480x360?text=TikTok+Video',
                        'width': 480,
                        'height': 360
                    }
                },
                'tags': ['tiktok', 'viral', query],
                'statistics': {
                    'viewCount': view_count,
                    'likeCount': like_count,
                    'commentCount': comment_count,
                    'subscriberCount': subscriber_count,
                    'viewSubscriberRatio': round(ratio, 2)
                }
            }
            videos.append(video_data)

        return {
            "videos": videos,
            "total": len(videos),
            "query": query,
            "order": order,
            "nextPageToken": "mock_next_page_token" if len(videos) == max_results else None
        }

    def _search_rapidapi(
        self,
        api_key: str,
        query: str,
        max_results: int,
        order: str,
        published_after: Optional[str],
        video_duration: Optional[str],
        min_ratio: Optional[float],
        min_comments: Optional[int],
        tag: Optional[str],
        page_token: Optional[str]
    ) -> Dict:
        """
        Execute search using RapidAPI (TikTok All-in-One or similar)
        """
        url = f"https://{Settings().tiktok_rapidapi_host}/search"
        
        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": Settings().tiktok_rapidapi_host
        }
        
        params = {
            "query": query,
            "page": 1, # Simplified pagination
            "sort_type": 0 # 0: Relevance, 1: Like, 2: Date
        }
        
        if order == 'date':
            params['sort_type'] = 2
        elif order == 'likes':
            params['sort_type'] = 1
            
        try:
            # Note: This is a hypothetical endpoint structure. 
            # Real RapidAPI endpoints vary significantly.
            # This is a template for the user to adjust based on their chosen provider.
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Map response to our format
            videos = []
            items = data.get('aweme_list', []) # Common field name in TikTok APIs
            
            for item in items:
                # Extract fields (safely)
                stats = item.get('statistics', {})
                author = item.get('author', {})
                
                view_count = stats.get('play_count', 0)
                subscriber_count = author.get('follower_count', 0)
                
                ratio = 0
                if subscriber_count > 0:
                    ratio = (view_count / subscriber_count) * 100
                    
                # Filter logic
                if min_ratio is not None and ratio < min_ratio:
                    continue
                
                video_data = {
                    'id': item.get('aweme_id'),
                    'title': item.get('desc', ''),
                    'description': item.get('desc', ''),
                    'channelTitle': author.get('nickname', 'Unknown'),
                    'publishedAt': datetime.fromtimestamp(item.get('create_time', 0)).isoformat() + "Z",
                    'thumbnails': {
                        'default': {'url': item.get('video', {}).get('cover', {}).get('url_list', [''])[0]},
                        'medium': {'url': item.get('video', {}).get('cover', {}).get('url_list', [''])[0]},
                        'high': {'url': item.get('video', {}).get('cover', {}).get('url_list', [''])[0]}
                    },
                    'tags': [], # Extraction depends on API
                    'statistics': {
                        'viewCount': view_count,
                        'likeCount': stats.get('digg_count', 0),
                        'commentCount': stats.get('comment_count', 0),
                        'subscriberCount': subscriber_count,
                        'viewSubscriberRatio': round(ratio, 2)
                    }
                }
                videos.append(video_data)
                
            return {
                "videos": videos,
                "total": len(videos),
                "query": query,
                "order": order,
                "nextPageToken": str(params['page'] + 1) if len(videos) > 0 else None
            }
            
        except Exception as e:
            print(f"RapidAPI Error: {e}")
            # Fallback to empty list or re-raise
            return {"videos": [], "total": 0, "error": str(e)}
    
    def get_video_details(self, video_id: str) -> Optional[Dict]:
        """
        Get detailed information about a specific video
        """
        api_key = Settings.get_tiktok_api_key()
        if api_key:
            # Implement real detail fetch here if needed
            pass

        # Mock implementation
        return {
            'id': video_id,
            'title': f'TikTok Video Details {video_id}',
            'description': 'Detailed description of the TikTok video.',
            'channelTitle': 'TikTokUser_Details',
            'publishedAt': datetime.utcnow().isoformat("T") + "Z",
            'thumbnails': {
                'medium': {
                    'url': 'https://placehold.co/320x180?text=TikTok+Detail',
                    'width': 320,
                    'height': 180
                },
                'high': {
                    'url': 'https://placehold.co/480x360?text=TikTok+Detail',
                    'width': 480,
                    'height': 360
                }
            },
            'statistics': {
                'viewCount': 50000,
                'likeCount': 2500,
                'commentCount': 100
            }
        }

tiktok_service = TikTokService()
