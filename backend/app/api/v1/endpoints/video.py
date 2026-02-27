from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from app.schemas.video import VideoCreate, VideoResponse
from app.worker import process_video_task
from app.core.redis_client import redis_client
import uuid
import json
import asyncio
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/generate", response_model=VideoResponse)
async def generate_video(request: VideoCreate):
    """
    Starts a video generation task and returns the task ID.
    """
    task_id = str(uuid.uuid4())
    
    # Initialize task state in Redis
    initial_state = {
        "id": task_id,
        "task_id": task_id,
        "status": "pending",
        "progress": 0,
        "message": "Task queued"
    }
    await redis_client.set(f"task:{task_id}", json.dumps(initial_state), ex=3600)
    
    # Trigger Celery task
    process_video_task.delay(task_id, request.prompt)
    
    return VideoResponse(**initial_state)

@router.get("/status/{task_id}", response_model=VideoResponse)
async def get_task_status(task_id: str):
    """
    Retrieves the current status of a task from Redis.
    """
    task_data = await redis_client.get(f"task:{task_id}")
    if not task_data:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return VideoResponse(**json.loads(task_data))

@router.get("/stream/{task_id}")
async def stream_task_progress(task_id: str, request: Request):
    """
    Streams task progress updates using Server-Sent Events (SSE).
    """
    async def event_generator():
        # First, send the current state if available
        task_data = await redis_client.get(f"task:{task_id}")
        if task_data:
            yield f"data: {task_data}\n\n"
        
        # Subscribe to PubSub for updates
        pubsub = redis_client.pubsub()
        await pubsub.subscribe(f"stream:{task_id}")
        
        try:
            while True:
                # Check if client disconnected
                if await request.is_disconnected():
                    break
                
                message = await pubsub.get_message(ignore_subscribe_message=True, timeout=1.0)
                if message:
                    data = message["data"]
                    yield f"data: {data}\n\n"
                    
                    # If task is finished, stop streaming
                    try:
                        status_data = json.loads(data)
                        if status_data.get("status") in ["completed", "failed"]:
                            break
                    except:
                        pass
                
                await asyncio.sleep(0.1)
        finally:
            await pubsub.unsubscribe(f"stream:{task_id}")
            await pubsub.close()

    return StreamingResponse(event_generator(), media_type="text/event-stream")
