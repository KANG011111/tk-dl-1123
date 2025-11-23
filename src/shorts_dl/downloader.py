from __future__ import annotations

import asyncio
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List

from yt_dlp import YoutubeDL  # type: ignore

from .config import settings

BEST_MP4_FORMAT = (
    "best[width=720]/"
    "best[height=720]/"
    "bestvideo[width=720][ext=mp4]+bestaudio[ext=m4a]/"
    "bestvideo[height=720][ext=mp4]+bestaudio[ext=m4a]/"
    "bestvideo[width=720]+bestaudio/"
    "bestvideo[height=720]+bestaudio/"
    "bestvideo[ext=mp4][vcodec^=avc1]+bestaudio[ext=m4a]/"
    "bestvideo[ext=mp4]+bestaudio[ext=m4a]/"
    "best[ext=mp4]/"
    "best"
)


def _base_opts(output_template: Path) -> Dict[str, Any]:
    return {
        "format": BEST_MP4_FORMAT,
        "outtmpl": str(output_template),
        "restrictfilenames": True,
        "quiet": True,
        "noprogress": True,
        "merge_output_format": "mp4",
    }


def _relative_download_path(path: Path) -> str:
    try:
        rel = path.relative_to(settings.downloads_dir)
    except ValueError:
        rel = path
    return f"/downloads/{rel.as_posix()}"


async def download_single_video(url: str) -> Dict[str, str]:
    downloads_dir = settings.downloads_dir
    downloads_dir.mkdir(parents=True, exist_ok=True)
    file_stem = f"{int(time.time())}_{uuid.uuid4().hex[:6]}"
    output_template = downloads_dir / f"{file_stem}.%(ext)s"

    def _task() -> Dict[str, str]:
        with YoutubeDL(_base_opts(output_template)) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title", "")
            final_path = Path(ydl.prepare_filename(info))
        return {"title": title, "file_url": _relative_download_path(final_path)}

    return await asyncio.to_thread(_task)


async def download_creator_batch(url: str, max_videos: int) -> List[Dict[str, str]]:
    downloads_dir = settings.downloads_dir
    timestamp = int(time.time())
    batch_dir = downloads_dir / f"creator_{timestamp}"
    batch_dir.mkdir(parents=True, exist_ok=True)
    output_template = batch_dir / "%(title).200s.%(ext)s"

    def _task() -> List[Dict[str, str]]:
        opts = _base_opts(output_template)
        opts.update(
            {
                "noplaylist": False,
                "playlistend": max_videos,
            }
        )
        with YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            entries = info.get("entries") or [info]
            results: List[Dict[str, str]] = []
            for entry in entries:
                if entry is None:
                    continue
                final_path = Path(ydl.prepare_filename(entry))
                results.append(
                    {
                        "title": entry.get("title", "Untitled"),
                        "file_url": _relative_download_path(final_path),
                    }
                )
                if len(results) >= max_videos:
                    break
            return results

    return await asyncio.to_thread(_task)


async def fetch_channel_videos(url: str) -> List[Dict[str, str]]:
    def _task() -> List[Dict[str, str]]:
        opts = {
            "extract_flat": True,
            "quiet": True,
            "noprogress": True,
        }
        with YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
            entries = info.get("entries") or []
            results: List[Dict[str, str]] = []
            for entry in entries:
                if entry is None:
                    continue
                results.append(
                    {
                        "title": entry.get("title", "Untitled"),
                        "url": entry.get("url") or entry.get("webpage_url") or "",
                        "id": entry.get("id", ""),
                    }
                )
            return results

    return await asyncio.to_thread(_task)


# Global dictionary to store cancellation events for batches
batch_cancellation_events: Dict[str, asyncio.Event] = {}

async def download_videos_batch_gen(urls: List[str], batch_id: str):
    downloads_dir = settings.downloads_dir
    timestamp = int(time.time())
    # Use batch_id in directory name if possible, or keep timestamp
    batch_dir = downloads_dir / f"batch_{batch_id}_{timestamp}"
    batch_dir.mkdir(parents=True, exist_ok=True)
    output_template = batch_dir / "%(title).200s.%(ext)s"
    
    opts = _base_opts(output_template)
    total = len(urls)

    # Register cancellation event
    cancel_event = asyncio.Event()
    batch_cancellation_events[batch_id] = cancel_event

    try:
        for i, url in enumerate(urls, 1):
            # Check for cancellation
            if cancel_event.is_set():
                yield {
                    "status": "cancelled",
                    "current": i - 1,
                    "total": total,
                    "message": "Batch download cancelled by user"
                }
                break

            try:
                # Run single download in thread to avoid blocking
                result = await asyncio.to_thread(_download_one, url, opts)
                yield {
                    "status": "progress",
                    "current": i,
                    "total": total,
                    "video": result
                }
            except Exception as e:
                yield {
                    "status": "error",
                    "current": i,
                    "total": total,
                    "message": str(e)
                }
                
        if not cancel_event.is_set():
            yield {"status": "completed"}
            
    finally:
        # Cleanup
        batch_cancellation_events.pop(batch_id, None)

async def download_video_to_batch(url: str, batch_id: str) -> Dict[str, str]:
    downloads_dir = settings.downloads_dir
    batch_dir = downloads_dir / batch_id
    batch_dir.mkdir(parents=True, exist_ok=True)
    output_template = batch_dir / "%(title).200s.%(ext)s"
    
    opts = _base_opts(output_template)
    return await asyncio.to_thread(_download_one, url, opts)


def _download_one(url: str, opts: Dict[str, Any]) -> Dict[str, str]:
    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        final_path = Path(ydl.prepare_filename(info))
        return {
            "title": info.get("title", "Untitled"),
            "file_url": _relative_download_path(final_path),
        }
