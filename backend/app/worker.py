import asyncio
import json
import logging
from app.core.celery_app import celery_app
from app.services.script_service import script_service
from app.services.voice_service import voice_service
from app.services.visual_service import visual_service
from app.services.engine_service import engine_service
from app.services.storage_service import storage_service
from app.core.redis_client import redis_client

logger = logging.getLogger(__name__)

async def update_task_progress(task_id: str, status: str, progress: int, message: str, data: dict = None):
    """
    Updates task status in Redis and publishes to PubSub channel.
    """
    payload = {
        "task_id": task_id,
        "status": status,
        "progress": progress,
        "message": message,
        "data": data or {}
    }
    # Store state in Redis
    await redis_client.set(f"task:{task_id}", json.dumps(payload), ex=3600)  # Expire in 1 hour
    # Publish to PubSub
    await redis_client.publish(f"stream:{task_id}", json.dumps(payload))

async def run_video_pipeline(task_id: str, prompt: str):
    try:
        await update_task_progress(task_id, "processing", 10, "Generating script...")
        
        # 1. Script
        script_data = await script_service.generate_script(prompt)
        if "error" in script_data:
            await update_task_progress(task_id, "failed", 0, f"Script Error: {script_data['error']}")
            return

        await update_task_progress(task_id, "processing", 20, "Generating voiceover...", {"title": script_data.get("title")})

        # 2. Voice
        audio_filename = f"{task_id}_audio.mp3"
        audio_path = await voice_service.generate_voiceover(script_data, audio_filename)
        
        if audio_path.startswith("Error"):
            await update_task_progress(task_id, "failed", 0, f"Voice Error: {audio_path}")
            return
        
        await update_task_progress(task_id, "processing", 40, "Fetching visual assets...")
        
        # 3. Visuals (Video Clips)
        scenes_with_visuals = await visual_service.fetch_video_clips_for_scenes(script_data["scenes"])
        
        await update_task_progress(task_id, "processing", 60, "Assembling video (rendering)...")

        # 4. Smart Assembly
        output_file = f"{task_id}_final.mp4"
        local_video_path, used_visual_paths = await engine_service.assemble_video(audio_path, scenes_with_visuals, output_file)
        
        await update_task_progress(task_id, "processing", 80, "Optimizing and uploading...")

        # 5. Extract/Search Thumbnail
        thumbnail_filename = f"{task_id}_thumb.jpg"
        thumb_keywords = script_data.get("thumbnail_keywords", [])
        local_thumb_path = None
        
        if thumb_keywords:
            local_thumb_path = await visual_service.fetch_thumbnail_image(thumb_keywords)
        
        if not local_thumb_path:
            local_thumb_path = await engine_service.extract_thumbnail(local_video_path, thumbnail_filename)
        
        if local_thumb_path:
            used_visual_paths.append(local_thumb_path)

        # 6. Cleanup unused visuals
        await visual_service.cleanup_unused_visuals(used_visual_paths)
        
        # 7. Upload to Cloud
        cloud_url = await storage_service.upload_video(local_video_path)
        cloud_thumb_url = None
        if local_thumb_path:
            cloud_thumb_url = await storage_service.upload_thumbnail(local_thumb_path)
        
        # 8. Update Final Status
        await update_task_progress(task_id, "completed", 100, "Video generated successfully!", {
            "video_url": cloud_url,
            "thumbnail_url": cloud_thumb_url
        })

    except Exception as e:
        logger.error(f"Worker Error: {e}")
        await update_task_progress(task_id, "failed", 0, f"System Error: {str(e)}")

@celery_app.task(name="app.worker.process_video_task")
def process_video_task(task_id: str, prompt: str):
    """
    Celery task wrapper for the async pipeline.
    """
    return asyncio.run(run_video_pipeline(task_id, prompt))
