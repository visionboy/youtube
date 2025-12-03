from fastapi import APIRouter, Query, HTTPException
from services.youtube_service import youtube_service
from typing import Optional

router = APIRouter(prefix="/api/videos", tags=["videos"])

@router.get("/search")
async def search_videos(
    q: str = Query(..., description="Search query"),
    maxResults: int = Query(25, ge=1, le=50, description="Maximum results"),
    order: str = Query("relevance", description="Sort order: date, rating, relevance, viewCount")
):
    """
    Search for YouTube videos with filters
    """
    try:
        result = youtube_service.search_videos(
            query=q,
            max_results=maxResults,
            order=order
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
        video = youtube_service.get_video_details(video_id)
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        return video
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
