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
        current_progress = 0
        
        async def log_step(message: str, progress_inc: int = 0):
            nonlocal current_progress
            current_progress = min(99, current_progress + progress_inc)
            await update_task_progress(task_id, "processing", current_progress, message)

        await log_step("Generating script...", 10)
        
        # 1. Script
        script_data = await script_service.generate_script(prompt)
        if "error" in script_data:
            await update_task_progress(task_id, "failed", 0, f"Script Error: {script_data['error']}")
            return

        await log_step(f"Script ready: {script_data.get('title', 'Video')}", 5)
        await log_step("Generating voiceover...", 10)

        # 2. Voice
        audio_filename = f"{task_id}_audio.mp3"
        audio_path = await voice_service.generate_voiceover(script_data, audio_filename)
        
        if audio_path.startswith("Error"):
            await update_task_progress(task_id, "failed", 0, f"Voice Error: {audio_path}")
            return
        
        await log_step("Voiceover generated.", 5)
        await log_step("Fetching visual assets...", 5)
        
        # 3. Visuals (Video Clips)
        scenes_with_visuals = await visual_service.fetch_video_clips_for_scenes(
            script_data["scenes"], 
            log_callback=lambda msg: log_step(msg, 2)
        )
        
        await log_step("Visual assets ready.", 5)

        # 4. Smart Assembly
        output_file = f"{task_id}_final.mp4"
        local_video_path, used_visual_paths = await engine_service.assemble_video(
            audio_path, 
            scenes_with_visuals, 
            output_file,
            log_callback=lambda msg: log_step(msg, 2)
        )
        
        await log_step("Video rendered.", 10)
        await log_step("Extracting thumbnail...", 5)

        # 5. Extract/Search Thumbnail
        thumbnail_filename = f"{task_id}_thumb.jpg"
        thumb_keywords = script_data.get("thumbnail_keywords", [])
        local_thumb_path = None
        
        if thumb_keywords:
            local_thumb_path = await visual_service.fetch_thumbnail_image(
                thumb_keywords,
                log_callback=lambda msg: log_step(msg, 1)
            )
        
        if not local_thumb_path:
            local_thumb_path = await engine_service.extract_thumbnail(local_video_path, thumbnail_filename)
        
        if local_thumb_path:
            used_visual_paths.append(local_thumb_path)

        # 6. Cleanup unused visuals
        await log_step("Cleaning up temporary files...", 2)
        await visual_service.cleanup_unused_visuals(used_visual_paths)
        
        # 7. Upload to Cloud
        await log_step("Uploading video...", 5)
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
