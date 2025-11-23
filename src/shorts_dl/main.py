from __future__ import annotations


import json
import uuid
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from yt_dlp.utils import DownloadError  # type: ignore

from .config import settings
from .schemas import (
    BatchDownloadRequest,
    CreatorDownloadRequest,
    CreatorDownloadResponse,
    ErrorResponse,
    FetchVideosRequest,
    FetchVideosResponse,
    SingleDownloadRequest,
    SingleDownloadResponse,
    BatchItemRequest,
    DownloadResult,
    StopBatchResponse,
)
from .downloader import (
    batch_cancellation_events,
    download_creator_batch,
    download_single_video,
    download_video_to_batch,
    download_videos_batch_gen,
    fetch_channel_videos,
)

app = FastAPI(title=settings.app_name)
app.mount("/downloads", StaticFiles(directory=settings.downloads_dir), name="downloads")


@app.get("/", response_class=HTMLResponse)
async def root() -> HTMLResponse:
    index_path = Path("public/index.html")
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="Landing page missing")
    return HTMLResponse(index_path.read_text(encoding="utf-8"))


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/download-single", response_model=SingleDownloadResponse)
async def download_single(payload: SingleDownloadRequest):
    try:
        result = await download_single_video(str(payload.url))
        return SingleDownloadResponse(title=result["title"], file_url=result["file_url"])
    except DownloadError as exc:  # pragma: no cover - network heavy path
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(message=f"下載失敗：{exc}").model_dump(),
        )
    except Exception as exc:  # pragma: no cover - defensive
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(message=f"unexpected_error: {exc}").model_dump(),
        )


@app.post("/api/download-creator", response_model=CreatorDownloadResponse)
async def download_creator(payload: CreatorDownloadRequest):
    try:
        videos_data = await download_creator_batch(
            url=str(payload.creator_url), max_videos=payload.max_videos
        )
        if not videos_data:
            return JSONResponse(
                status_code=404,
                content=ErrorResponse(message="抓不到任何影片").model_dump(),
            )
        # Convert dicts to Pydantic models to satisfy mypy
        from .schemas import DownloadResult

        videos = [DownloadResult(**v) for v in videos_data]
        return CreatorDownloadResponse(videos=videos)
    except DownloadError as exc:  # pragma: no cover - network heavy path
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(message=f"下載失敗：{exc}").model_dump(),
        )
    except Exception as exc:  # pragma: no cover - defensive
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(message=f"unexpected_error: {exc}").model_dump(),
        )


@app.post("/api/fetch-videos", response_model=FetchVideosResponse)
async def fetch_videos(payload: FetchVideosRequest):
    try:
        videos_data = await fetch_channel_videos(str(payload.creator_url))
        # Convert to Pydantic models
        from .schemas import VideoInfo
        videos = [VideoInfo(**v) for v in videos_data]
        return FetchVideosResponse(videos=videos)
    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(message=f"Failed to fetch videos: {exc}").model_dump(),
        )


@app.post("/api/download-batch", response_class=StreamingResponse)
async def download_batch(payload: BatchDownloadRequest):
    if len(payload.video_urls) < 5:
            return JSONResponse(
            status_code=400,
            content=ErrorResponse(message=f"最少需要選擇 5 支影片，目前選擇 {len(payload.video_urls)} 支").model_dump(),
        )
    
    urls = [str(url) for url in payload.video_urls]
    batch_id = payload.batch_id or uuid.uuid4().hex
    
    async def event_generator():
        async for progress in download_videos_batch_gen(urls, batch_id):
            yield json.dumps(progress) + "\n"

    return StreamingResponse(event_generator(), media_type="application/x-ndjson")


@app.post("/api/stop-batch/{batch_id}", response_model=StopBatchResponse)
async def stop_batch(batch_id: str):
    if batch_id in batch_cancellation_events:
        batch_cancellation_events[batch_id].set()
        return StopBatchResponse(status="success", message=f"Batch {batch_id} stopping...")
    return StopBatchResponse(status="error", message=f"Batch {batch_id} not found")

@app.post("/api/download-batch-item")
async def download_batch_item(payload: BatchItemRequest):
    try:
        video_data = await download_video_to_batch(str(payload.url), payload.batch_id)
        from .schemas import DownloadResult
        return DownloadResult(**video_data)
    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(message=f"Download failed: {exc}").model_dump(),
        )
