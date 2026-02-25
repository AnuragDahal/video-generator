from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.schemas.video import VideoCreate, VideoResponse
from app.services.script_service import script_service
from app.services.voice_service import voice_service
from app.services.visual_service import visual_service
from app.services.engine_service import engine_service
from app.services.storage_service import storage_service
import uuid
import os
from typing import Dict

router = APIRouter()

# In-memory store for task status 
# In production, use Redis or a Database
tasks_db: Dict[str, VideoResponse] = {}

async def process_video_task(task_id: str, prompt: str):
    """
    Background worker that runs the full pipeline and updates the tasks_db.
    """
    try:
        tasks_db[task_id].status = "processing"
        
        # 1. Script
        script_data = await script_service.generate_script(prompt)
        if "error" in script_data:
            tasks_db[task_id].status = "failed"
            tasks_db[task_id].error = script_data["error"]
            return

        tasks_db[task_id].script = script_data
        tasks_db[task_id].title = script_data.get("title")

        # 2. Voice
        audio_filename = f"{task_id}_audio.mp3"
        audio_path = await voice_service.generate_voiceover(script_data, audio_filename)
        
        if audio_path.startswith("Error"):
            tasks_db[task_id].status = "failed"
            tasks_db[task_id].error = audio_path
            return
        
        # 3. Visuals (Video Clips)
        scenes_with_visuals = await visual_service.fetch_video_clips_for_scenes(script_data["scenes"])
        
        # 4. Smart Assembly
        output_file = f"{task_id}_final.mp4"
        local_video_path, used_visual_paths = await engine_service.assemble_video(audio_path, scenes_with_visuals, output_file)
        
        # 5. Extract/Search Thumbnail
        print("🖼️ Generating thumbnail...")
        thumbnail_filename = f"{task_id}_thumb.jpg"
        
        # Try to search for a relevant image first
        thumb_keywords = script_data.get("thumbnail_keywords", [])
        local_thumb_path = None
        
        if thumb_keywords:
            local_thumb_path = await visual_service.fetch_thumbnail_image(thumb_keywords)
        
        # Fallback to extracting from video if search fails or no keywords
        if not local_thumb_path:
            print("⚠️ No thumbnail image found, falling back to video extraction...")
            local_thumb_path = await engine_service.extract_thumbnail(local_video_path, thumbnail_filename)
        
        # Add local thumb path to used visuals for cleanup safety (optional but good practice)
        if local_thumb_path:
            used_visual_paths.append(local_thumb_path)

        # 6. Cleanup unused visuals
        await visual_service.cleanup_unused_visuals(used_visual_paths)
        
        # 7. Upload to Cloud
        print(f"Uploading {local_video_path} to cloud...")
        cloud_url = await storage_service.upload_video(local_video_path)
        
        cloud_thumb_url = None
        if local_thumb_path:
            print(f"Uploading {local_thumb_path} to cloud...")
            cloud_thumb_url = await storage_service.upload_thumbnail(local_thumb_path)
        
        # 8. Update Final Status
        tasks_db[task_id].video_url = cloud_url
        tasks_db[task_id].thumbnail_url = cloud_thumb_url
        tasks_db[task_id].status = "completed"
        print(f"Task {task_id} completed successfully.")

    except Exception as e:
        print(f"Background Task Error: {e}")
        tasks_db[task_id].status = "failed"
        tasks_db[task_id].error = str(e)

@router.post("/generate", response_model=VideoResponse)
async def generate_video(request: VideoCreate, background_tasks: BackgroundTasks):
    # Create unique task ID
    task_id = str(uuid.uuid4())
    
    # Initialize task status
    task_response = VideoResponse(
        id=task_id,
        task_id=task_id,
        status="pending",
    )
    tasks_db[task_id] = task_response
    
    # Run heavy work in background
    background_tasks.add_task(process_video_task, task_id, request.prompt)
    
    return task_response

@router.get("/status/{task_id}", response_model=VideoResponse)
async def get_task_status(task_id: str):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return tasks_db[task_id]
