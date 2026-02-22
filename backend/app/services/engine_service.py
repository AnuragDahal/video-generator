import os
from pathlib import Path
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
from app.core.config import settings

class EngineService:
    def __init__(self):
        self.output_dir = Path(settings.OUTPUT_DIR)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def assemble_video(self, audio_path: str, visual_paths: list[str], output_filename: str) -> str:
        """
        Combines audio and visuals into a final high-quality .mp4 file.
        Uses MoviePy 2.x syntax.
        """
        if not visual_paths:
            raise ValueError("No visual paths provided for video assembly.")
        
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        print(f"Assembling video: {output_filename}")
        
        try:
            # 1. Load Audio and get total duration
            audio_clip = AudioFileClip(audio_path)
            total_duration = audio_clip.duration
            
            # 2. Calculate duration per image
            num_images = len(visual_paths)
            duration_per_image = total_duration / num_images
            
            clips = []
            
            # 3. Create image clips with effects
            for img_path in visual_paths:
                if not os.path.exists(img_path):
                    print(f"Warning: Image not found, skipping: {img_path}")
                    continue
                
                # Create a clip and set its duration using MoviePy 2.x syntax
                # In 2.x: .with_duration() instead of .set_duration()
                clip = ImageClip(img_path).with_duration(duration_per_image)
                
                # Resize and crop logic using MoviePy 2.x syntax
                # .resized() instead of .resize()
                clip = clip.resized(height=1080)
                if clip.w < 1920:
                    clip = clip.resized(width=1920)
                
                # .cropped() instead of .crop()
                clip = clip.cropped(x_center=clip.w/2, y_center=clip.h/2, width=1920, height=1080)
                
                clips.append(clip)

            if not clips:
                if audio_clip: audio_clip.close()
                raise ValueError("No valid image clips could be created.")

            # 4. Concatenate and set audio using MoviePy 2.x syntax
            final_video = concatenate_videoclips(clips, method="compose")
            final_video = final_video.with_audio(audio_clip) # .with_audio() instead of .set_audio()
            
            # 5. Write output
            output_path = self.output_dir / output_filename
            
            # Use high quality settings
            final_video.write_videofile(
                str(output_path),
                fps=24,
                codec="libx264",
                audio_codec="aac",
                logger=None 
            )
            
            # 6. Cleanup
            audio_clip.close()
            for clip in clips:
                clip.close()
            final_video.close()

            print(f"Successfully assembled video: {output_path}")
            return str(output_path)

        except Exception as e:
            print(f"Error in video assembly: {e}")
            raise e

engine_service = EngineService()
