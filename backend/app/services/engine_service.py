import os
import multiprocessing
from pathlib import Path
from moviepy import ImageClip, AudioFileClip, VideoFileClip, concatenate_videoclips
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
            used_visual_paths = set()
            
            # 3. Create clips for each scene
            for i, scene in enumerate(scenes):
                narration_text = scene.get("narration_part", "")
                
                # Check for video clips first, then fallback to images
                video_paths = scene.get("video_paths", [])
                image_paths = scene.get("image_paths", [])
                
                # Calculate scene duration proportional to text length
                char_ratio = len(narration_text) / total_chars if total_chars > 0 else 1/len(scenes)
                scene_duration = char_ratio * total_duration
                
                if not video_paths and not image_paths:
                    print(f"Warning: Scene {i+1} has no visual assets. Skipping.")
                    continue
                
                if video_paths:
                    # Logic for Video Clips
                    duration_per_clip = scene_duration / len(video_paths)
                    for vid_path in video_paths:
                        if not os.path.exists(vid_path):
                            continue
                        
                        clip = VideoFileClip(vid_path)
                        used_visual_paths.add(vid_path)
                        
                        # Trim video to match required duration
                        # Use a tiny safety margin (0.01) to avoid MoviePy last-frame read errors
                        if clip.duration > duration_per_clip:
                            clip = clip.subclipped(0, min(duration_per_clip, clip.duration - 0.01))
                        else:
                            # If clip is too short, we fill the duration (MoviePy loops the last frame by default)
                            clip = clip.with_duration(duration_per_clip)
                        
                        # High-speed Resize & Crop for consistency
                        clip = clip.resized(height=720)
                        if clip.w < 1280:
                            clip = clip.resized(width=1280)
                        clip = clip.cropped(x_center=clip.w/2, y_center=clip.h/2, width=1280, height=720)
                        
                        clips.append(clip)
                
                else:
                    # Logic for Static Images (Fallback)
                    duration_per_image = scene_duration / len(image_paths)
                    for img_path in image_paths:
                        if not os.path.exists(img_path):
                            continue
                        
                        clip = ImageClip(img_path).with_duration(duration_per_image)
                        used_visual_paths.add(img_path)
                        
                        # High-speed Resize & Crop
                        clip = clip.resized(height=720)
                        if clip.w < 1280:
                            clip = clip.resized(width=1280)
                        clip = clip.cropped(x_center=clip.w/2, y_center=clip.h/2, width=1280, height=720)
                        
                        clips.append(clip)

            if not clips:
                audio_clip.close()
                raise ValueError("No valid clips created. Check if visuals were downloaded.")

            # 4. Concatenate and Finish
            # 'chain' is MUCH more memory efficient than 'compose'
            # It works here because we've normalized all clips to 1280x720 above
            final_video = concatenate_videoclips(clips, method="chain")
            final_video = final_video.with_audio(audio_clip)
            
            output_path = self.output_dir / output_filename
            
            # Limit threads to 2 to prevent memory spikes in parallel encoding
            render_threads = min(2, self.cpu_count)
            
            final_video.write_videofile(
                str(output_path),
                fps=24,
                codec="libx264",
                audio_codec="aac",
                threads=render_threads,
                preset="ultrafast",
                logger=None 
            )
            
            # Cleanup
            audio_clip.close()
            for clip in clips:
                clip.close()
            final_video.close()

            print(f"✅ Smart assembly completed: {output_path}")
            return str(output_path), list(used_visual_paths)

        except Exception as e:
            print(f"❌ Smart assembly failed: {e}")
            raise e

    async def extract_thumbnail(self, video_path: str, output_filename: str) -> str:
        """
        Extracts a frame from the video to use as a thumbnail.
        Defaults to the first second or middle of the video.
        """
        try:
            print(f"🖼️ Extracting thumbnail for: {video_path}")
            clip = VideoFileClip(video_path)
            
            # Take a frame at 1 second, or middle if video is shorter than 1s
            t = min(1.0, clip.duration / 2)
            
            output_path = self.output_dir / output_filename
            clip.save_frame(str(output_path), t=t)
            
            clip.close()
            return str(output_path)
        except Exception as e:
            print(f"❌ Thumbnail extraction failed: {e}")
            return None

engine_service = EngineService()
