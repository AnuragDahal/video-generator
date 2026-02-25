from app.core.config import settings
from app.services.engine_service import engine_service
from app.services.visual_service import visual_service
from app.services.voice_service import voice_service
from app.services.script_service import script_service
import asyncio
import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Load env before imports
load_dotenv()


async def test_automated_video_pipeline():
    print("🚀 Starting Automated Smart-Sync Video Pipeline...")
    output_path = Path(settings.OUTPUT_DIR) / "scripts"
    output_path.mkdir(parents=True, exist_ok=True)
    prompt = input('Enter your prompt: ')
    video_id = input('Enter your video id: ')

    try:
        # 1. Script
        print("\n--- Step 1: Generating Script ---")
        script_data = await script_service.generate_script(prompt)
        with open(output_path / f'{video_id}_script.json', 'w') as f:
            json.dump(script_data, f, indent=2)
        print(f"✅ Generated script with {len(script_data['scenes'])} scenes.")

        # 2. Voice
        print("\n--- Step 2: Generating Voiceover ---")
        audio_filename = f"{video_id}_audio.mp3"
        audio_path = await voice_service.generate_voiceover(script_data, audio_filename)
        print(f"✅ Audio generated: {audio_path}")

        # 3. Visuals (Scene-linked)
        print("\n--- Step 3: Fetching Scene-Linked Visuals ---")
        scenes_with_visuals = await visual_service.fetch_video_clips_for_scenes(script_data["scenes"])
        print("✅ Visuals fetched and linked to scenes.")

        # 4. Smart Assembly
        print("\n--- Step 4: Assembling with Smart Timing ---")
        output_filename = f"{video_id}_smart_sync.mp4"
        final_video_path, used_visuals = await engine_service.assemble_video(audio_path, scenes_with_visuals, output_filename)
        
        # 5. Thumbnail Generation (Search then Fallback)
        print("\n--- Step 5: Generating Thumbnail ---")
        thumb_keywords = script_data.get("thumbnail_keywords", [])
        thumbnail_path = None
        
        if thumb_keywords:
            print(f"Searching for thumbnail image with keywords: {thumb_keywords}")
            thumbnail_path = await visual_service.fetch_thumbnail_image(thumb_keywords)
        
        if not thumbnail_path:
            print("Falling back to video frame extraction...")
            thumbnail_filename = f"{video_id}_thumb.jpg"
            thumbnail_path = await engine_service.extract_thumbnail(final_video_path, thumbnail_filename)
            
        print(f"✅ Thumbnail ready: {thumbnail_path}")

        print("\n✨ PIPELINE SUCCESS ✨")
        print(f"Final Sync'd Video: {final_video_path}")
        print(f"Thumbnail: {thumbnail_path}")

    except Exception as e:
        print(f"\n❌ PIPELINE FAILED: {e}")

if __name__ == "__main__":
    asyncio.run(test_automated_video_pipeline())
