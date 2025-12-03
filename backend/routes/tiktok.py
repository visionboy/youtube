from fastapi import APIRouter, Query, HTTPException
from services.tiktok_service import tiktok_service
from typing import Optional

router = APIRouter(prefix="/api/tiktok", tags=["tiktok"])

@router.get("/search")
async def search_videos(
    q: str = Query(..., description="Search query"),
    maxResults: int = Query(25, ge=1, le=50, description="Maximum results"),
    order: str = Query("relevance", description="Sort order: date, rating, relevance, viewCount"),
    publishedAfter: Optional[str] = Query(None, description="Filter by date: 1m, 2m, 6m, 1y, all"),
    videoDuration: Optional[str] = Query(None, description="Filter by duration: short, long, any"),
    minRatio: Optional[float] = Query(None, description="Minimum views/subscriber ratio"),
    minComments: Optional[int] = Query(None, description="Minimum comment count"),
    tag: Optional[str] = Query(None, description="Filter by tag"),
    pageToken: Optional[str] = Query(None, description="Page token for pagination")
):
    """
    Search for TikTok videos with filters
    """
    try:
        result = tiktok_service.search_videos(
            query=q,
            max_results=maxResults,
            order=order,
            published_after=publishedAfter,
            video_duration=videoDuration,
            min_ratio=minRatio,
            min_comments=minComments,
            tag=tag,
            page_token=pageToken
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{video_id}")
async def get_video(video_id: str):
    """
    Get detailed information about a specific video
    """
    try:
        video = tiktok_service.get_video_details(video_id)
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        return video
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
