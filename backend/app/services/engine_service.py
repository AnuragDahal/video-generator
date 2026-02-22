import os
import multiprocessing
from pathlib import Path
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
from app.core.config import settings

class EngineService:
    def __init__(self):
        self.output_dir = Path(settings.OUTPUT_DIR)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.cpu_count = multiprocessing.cpu_count()

    async def assemble_video(self, audio_path: str, scenes: list[dict], output_filename: str) -> str:
        """
        Assembles video by syncing images to the duration of their respective narration parts.
        """
        if not scenes:
            raise ValueError("No scenes provided for video assembly.")
        
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        print(f"🎬 Smart-Assembling video: {output_filename}...")
        
        try:
            # 1. Load Audio and get total duration
            audio_clip = AudioFileClip(audio_path)
            total_duration = audio_clip.duration
            
            # 2. Calculate Total Narrative Length for proportional timing
            total_chars = sum(len(s.get("narration_part", "")) for s in scenes)
            if total_chars == 0:
                print("Warning: Narration parts are empty. Falling back to equal timing.")
                total_chars = len(scenes) # Fallback
            
            clips = []
            
            # 3. Create clips for each scene
            for i, scene in enumerate(scenes):
                narration_text = scene.get("narration_part", "")
                image_paths = scene.get("image_paths", [])
                
                # Calculate scene duration proportional to text length
                # CurrentSceneDuration = (SceneChars / TotalChars) * TotalAudioDuration
                char_ratio = len(narration_text) / total_chars if total_chars > 0 else 1/len(scenes)
                scene_duration = char_ratio * total_duration
                
                if not image_paths:
                    print(f"Warning: Scene {i+1} has no images. Using placeholder logic or skipping.")
                    continue
                
                # Split scene duration among scene images
                duration_per_image = scene_duration / len(image_paths)
                
                for img_path in image_paths:
                    if not os.path.exists(img_path):
                        continue
                    
                    clip = ImageClip(img_path).with_duration(duration_per_image)
                    
                    # High-speed Resize & Crop
                    clip = clip.resized(height=1080)
                    if clip.w < 1920:
                        clip = clip.resized(width=1920)
                    clip = clip.cropped(x_center=clip.w/2, y_center=clip.h/2, width=1920, height=1080)
                    
                    clips.append(clip)

            if not clips:
                audio_clip.close()
                raise ValueError("No valid clips created. Check if images were downloaded.")

            # 4. Concatenate and Finish
            final_video = concatenate_videoclips(clips, method="compose")
            final_video = final_video.with_audio(audio_clip)
            
            output_path = self.output_dir / output_filename
            
            final_video.write_videofile(
                str(output_path),
                fps=24,
                codec="libx264",
                audio_codec="aac",
                threads=self.cpu_count,
                preset="ultrafast",
                logger=None 
            )
            
            # Cleanup
            audio_clip.close()
            for clip in clips:
                clip.close()
            final_video.close()

            print(f"✅ Smart assembly completed: {output_path}")
            return str(output_path)

        except Exception as e:
            print(f"❌ Smart assembly failed: {e}")
            raise e

engine_service = EngineService()
