from __future__ import annotations

from fastapi.testclient import TestClient

from shorts_dl.main import app

client = TestClient(app)


def test_single_download_success(monkeypatch):
    async def fake_download_single(url: str):
        return {"title": "Demo", "file_url": "/downloads/demo.mp4"}

    monkeypatch.setattr(
        "shorts_dl.main.download_single_video", fake_download_single
    )

    resp = client.post("/api/download-single", json={"url": "https://example.com"})
    assert resp.status_code == 200
    payload = resp.json()
    assert payload["status"] == "success"
    assert payload["file_url"].endswith("demo.mp4")


def test_creator_download_success(monkeypatch):
    async def fake_download_batch(url: str, max_videos: int):
        return [
            {"title": "One", "file_url": "/downloads/x1.mp4"},
            {"title": "Two", "file_url": "/downloads/x2.mp4"},
        ]

    monkeypatch.setattr(
        "shorts_dl.main.download_creator_batch", fake_download_batch
    )

    resp = client.post(
        "/api/download-creator",
        json={"creator_url": "https://example.com", "max_videos": 2},
    )
    assert resp.status_code == 200
    payload = resp.json()
    assert payload["status"] == "success"
    assert len(payload["videos"]) == 2


def test_creator_download_empty(monkeypatch):
    async def fake_download_batch(url: str, max_videos: int):
        return []

    monkeypatch.setattr(
        "shorts_dl.main.download_creator_batch", fake_download_batch
    )

    resp = client.post(
        "/api/download-creator",
        json={"creator_url": "https://example.com", "max_videos": 5},
    )
    assert resp.status_code == 404
    payload = resp.json()
    assert payload["status"] == "error"
    assert "影片" in payload["message"]
