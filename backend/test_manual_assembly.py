import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

# Load env before imports
load_dotenv()

from app.services.engine_service import engine_service

async def test_manual_video_assembly():
    print("🎬 Starting Manual Video Assembly...")
    
    # Paths provided by the user
    audio_path = r"c:\Users\freef\OneDrive\Desktop\CodePlaygrond\personal\video-generator\backend\outputs\audio\pyramids_mystery_audio.mp3"
    visuals_dir = r"c:\Users\freef\OneDrive\Desktop\CodePlaygrond\personal\video-generator\backend\outputs\visuals"
    
    # Collect all image files from the visuals directory
    visual_paths = []
    if os.path.exists(visuals_dir):
        for file in os.listdir(visuals_dir):
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                visual_paths.append(os.path.join(visuals_dir, file))
    
    print(f"Found {len(visual_paths)} images in {visuals_dir}")
    
    if not visual_paths:
        print("❌ No images found to assemble video.")
        return

    if not os.path.exists(audio_path):
        print(f"❌ Audio file not found: {audio_path}")
        return
    
    try:
        print("\n--- Assembling Video using existing assets ---")
        output_filename = "pyramids_mystery_final_video_2.mp4"
        final_video_path = await engine_service.assemble_video(audio_path, visual_paths, output_filename)
        
        print("\n✨ ASSEMBLY SUCCESS ✨")
        print(f"Final Video File: {final_video_path}")
        
    except Exception as e:
        print(f"\n❌ ASSEMBLY FAILED: {e}")

if __name__ == "__main__":
    asyncio.run(test_manual_video_assembly())
