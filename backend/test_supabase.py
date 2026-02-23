import asyncio
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

from app.services.storage_service import storage_service

async def test_supabase_upload():
    print("🚀 Testing Supabase Storage Upload...")
    
    # Check if a test file exists, if not create a dummy one
    test_file = "test_upload.txt"
    with open(test_file, "w") as f:
        f.write("This is a test upload for the video generator project.")
    
    print(f"Created temporary file: {test_file}")
    
    try:
        # Attempt upload
        print("Attempting to upload to Supabase...")
        # Note: I'm using the .txt for testing, though the service is set for video/mp4
        # The service will try to upload it as a video/mp4 because of the hardcoded header
        # but Supabase usually doesn't care about the content-type matching for simple uploads.
        result_url = await storage_service.upload_video(test_file)
        
        if result_url and "http" in str(result_url):
            print(f"✅ Upload Success!")
            print(f"Public URL: {result_url}")
        else:
            print("❌ Upload failed or returned local path (check if SUPABASE_URL/KEY are set in .env)")
            print(f"Result: {result_url}")
            
    except Exception as e:
        print(f"❌ Exception during upload: {e}")
    finally:
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)
            print(f"Cleaned up {test_file}")

if __name__ == "__main__":
    asyncio.run(test_supabase_upload())
