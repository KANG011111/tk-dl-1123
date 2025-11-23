import asyncio
import random
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from shorts_dl.downloader import fetch_channel_videos, download_single_video

async def main():
    creator_url = "https://www.tiktok.com/@mibi_na"
    print(f"Fetching videos from: {creator_url}")
    
    try:
        videos = await fetch_channel_videos(creator_url)
        print(f"Found {len(videos)} videos.")
        
        if not videos:
            print("No videos found!")
            return

        # Randomly select 5 videos
        sample_size = min(5, len(videos))
        selected_videos = random.sample(videos, sample_size)
        
        print(f"Selected {sample_size} videos for download:")
        for v in selected_videos:
            print(f"- {v['title']} ({v['url']})")
            
        print("\nStarting downloads...")
        for v in selected_videos:
            print(f"Downloading: {v['title']}...")
            try:
                result = await download_single_video(v['url'])
                print(f"  -> Success: {result['file_url']}")
            except Exception as e:
                print(f"  -> Failed: {e}")
                
    except Exception as e:
        print(f"Error fetching videos: {e}")

if __name__ == "__main__":
    asyncio.run(main())
