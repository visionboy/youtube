from typing import List, Dict, Optional
import random
from datetime import datetime, timedelta

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
        Mock search for TikTok videos
        """
        # Mock data generation
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
    
    def get_video_details(self, video_id: str) -> Optional[Dict]:
        """
        Get detailed information about a specific video (Mock)
        """
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
