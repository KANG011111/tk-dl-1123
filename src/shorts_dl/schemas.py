from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, Field, HttpUrl

from .config import settings


class SingleDownloadRequest(BaseModel):
    url: HttpUrl


class DownloadResult(BaseModel):
    title: str
    file_url: str


class SingleDownloadResponse(BaseModel):
    status: Literal["success"] = "success"
    title: str
    file_url: str


class CreatorDownloadRequest(BaseModel):
    creator_url: HttpUrl
    max_videos: int = Field(
        default=settings.default_batch_videos,
        ge=settings.min_batch_videos,
        le=settings.max_batch_videos,
    )


class CreatorDownloadResponse(BaseModel):
    status: Literal["success"] = "success"
    videos: List[DownloadResult]


class ErrorResponse(BaseModel):
    status: Literal["error"] = "error"
    message: str


class VideoInfo(BaseModel):
    title: str
    url: str
    id: str


class FetchVideosRequest(BaseModel):
    creator_url: HttpUrl


class FetchVideosResponse(BaseModel):
    status: Literal["success"] = "success"
    videos: List[VideoInfo]


class BatchDownloadRequest(BaseModel):
    video_urls: List[HttpUrl]
    batch_id: Optional[str] = None

class BatchItemRequest(BaseModel):
    url: HttpUrl
    batch_id: str


class StopBatchResponse(BaseModel):
    status: Literal["success", "error"]
    message: str
