import asyncio
import os
from dotenv import load_dotenv
from app.services.visual_service import visual_service

# Load environment variables
load_dotenv()

async def test_video_fetching():
    print("Testing Pexels video clips Fetching...")
    # Using keywords from the user's Bermuda Triangle script
    keywords = ["Bermuda Triangle ocean", "Flight 19 plane", "Shipwreck", "Stormy Sea"]
    
    paths = await visual_service.fetch_video_clips(keywords)
    
    print("\nResults:")
    if paths:
        for path in paths:
            print(f"Success: {path}")
            if os.path.exists(path):
                print(f"File verified at: {path}")
            else:
                print(f"Error: File NOT found at: {path}")
    else:
        print("No video clips were downloaded.")

if __name__ == "__main__":
    asyncio.run(test_video_fetching())
