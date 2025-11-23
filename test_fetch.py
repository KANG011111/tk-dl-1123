import asyncio
from src.shorts_dl.downloader import fetch_channel_videos

async def main():
    url = "https://www.youtube.com/@LIGHTSAREOFF/shorts"
    print(f"Fetching from {url}...")
    try:
        videos = await fetch_channel_videos(url)
        print(f"Found {len(videos)} videos.")
        if videos:
            print(f"First video: {videos[0]}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
