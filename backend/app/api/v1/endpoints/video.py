from fastapi import APIRouter, HTTPException
from app.schemas.video import VideoCreate, VideoResponse
from app.services.script_service import script_service
from app.services.voice_service import voice_service
from app.services.visual_service import visual_service
from app.services.engine_service import engine_service

router = APIRouter()

@router.post("/generate", response_model=VideoResponse)
async def generate_video(request: VideoCreate):
    try:
        # Step 1: Generate Script
        script = await script_service.generate_script(request.prompt)
        
        # Step 2: Generate Voiceover
        audio_path = f"temp/audio_{request.prompt[:10]}.mp3"
        await voice_service.generate_voiceover(script, audio_path)
        
        # Step 3: Fetch Visuals
        visuals = await visual_service.fetch_visuals(["scenary", "tech"])
        
        # Step 4: Assemble Video
        output_file = f"video_{request.prompt[:10]}.mp4"
        video_path = await engine_service.assemble_video(audio_path, visuals, output_file)
        
        return VideoResponse(
            id="temp-id",
            status="completed",
            video_url=video_path,
            script=script
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
