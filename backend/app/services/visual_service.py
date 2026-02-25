import httpx
from typing import List, Dict, Optional
from pathlib import Path
from app.core.config import settings

class VisualService:
    def __init__(self):
        self.api_key = settings.PEXELS_API_KEY
        self.base_url = "https://api.pexels.com/v1"
        self.video_base_url = "https://api.pexels.com/videos"
        self.output_path = Path(settings.OUTPUT_DIR) / "visuals"
        self.output_path.mkdir(parents=True, exist_ok=True)


    # -------------------------------------------------------------------------
    # Scene-level orchestration
    # -------------------------------------------------------------------------

    async def fetch_video_clips_for_scenes(self, scenes: List[Dict]) -> List[Dict]:
        """
        Downloads a pool of best-match video clips per scene using all keywords.
        Attaches a list of local paths to each scene under 'video_paths'.
        """
        for i, scene in enumerate(scenes):
            keywords = scene.get("visual_keywords", [])
            print(f"🎬  Scene {i+1}: searching video clips with {len(keywords)} keyword(s)...")
            clips = await self._fetch_pool_of_videos(keywords)
            scene["video_paths"] = clips
            if not clips:
                print(f"  ⚠️  Scene {i+1}: no video clips found for any keyword.")
            else:
                print(f"  ✅ Scene {i+1}: found {len(clips)} clip(s).")
        return scenes

    # -------------------------------------------------------------------------
    # Fallback search — tries keywords one by one, stops at first good result
    # -------------------------------------------------------------------------


    async def _fetch_pool_of_videos(self, keywords: List[str], max_clips: int = 3) -> List[str]:
        """
        Searches across all keywords to build a variety of clips for a scene.
        Returns a list of local paths.
        """
        headers = {"Authorization": self.api_key}
        clips_found = []
        downloaded_ids = set()

        async with httpx.AsyncClient(timeout=60.0) as client:
            for keyword in keywords:
                if len(clips_found) >= max_clips:
                    break
                
                try:
                    response = await client.get(
                        f"{self.video_base_url}/search",
                        headers=headers,
                        params={"query": keyword, "per_page": 5, "orientation": "landscape"}
                    )
                    response.raise_for_status()
                    videos = response.json().get("videos", [])

                    if not videos:
                        continue

                    # Find the first video in results that we haven't already picked for this scene
                    for video in videos:
                        video_id = video["id"]
                        if video_id in downloaded_ids:
                            continue
                        
                        video_file = self._pick_best_video_file(video.get("video_files", []))
                        if not video_file:
                            continue

                        local_path = self._build_local_path(video_id, ".mp4")
                        downloaded_ids.add(video_id)

                        if local_path.exists():
                            print(f"  ✅ Cache hit for clip: '{keyword}'")
                            clips_found.append(str(local_path))
                            break # Move to next keyword

                        print(f"  ⬇️  Downloading clip for: '{keyword}'")
                        vid_response = await client.get(video_file["link"])
                        vid_response.raise_for_status()
                        local_path.write_bytes(vid_response.content)
                        clips_found.append(str(local_path))
                        break # Successfully got one from this keyword, move to next

                except Exception as e:
                    print(f"  ❌ Error for keyword '{keyword}': {e}")

        return clips_found

    async def fetch_thumbnail_image(self, keywords: List[str]) -> Optional[str]:
        """
        Searches for a high-quality image to use as a thumbnail based on keywords.
        Returns the local path to the downloaded image.
        """
        headers = {"Authorization": self.api_key}
        async with httpx.AsyncClient(timeout=30.0) as client:
            for keyword in keywords:
                try:
                    print(f"🖼️  Searching thumbnail image for: '{keyword}'")
                    response = await client.get(
                        f"{self.base_url}/search",
                        headers=headers,
                        params={"query": keyword, "per_page": 5, "orientation": "landscape"}
                    )
                    response.raise_for_status()
                    photos = response.json().get("photos", [])

                    if not photos:
                        continue

                    # Pick the first photo
                    photo = photos[0]
                    photo_id = photo["id"]
                    # Use the 'large' or 'original' size
                    image_url = photo.get("src", {}).get("large") or photo.get("src", {}).get("original")
                    
                    if not image_url:
                        continue

                    local_path = self._build_local_path(photo_id, ".jpg")
                    if local_path.exists():
                        return str(local_path)

                    print(f"  ⬇️  Downloading thumbnail image...")
                    img_response = await client.get(image_url)
                    img_response.raise_for_status()
                    local_path.write_bytes(img_response.content)
                    return str(local_path)

                except Exception as e:
                    print(f"  ❌ Error fetching thumbnail for '{keyword}': {e}")
        
        return None

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    def _build_local_path(self, media_id: int, ext: str) -> Path:
        return self.output_path / f"{media_id}{ext}"

    def _pick_best_video_file(self, video_files: list) -> Optional[dict]:
        """
        From a list of Pexels video file objects, prefer the HD version (720p/1080p).
        Falls back to the first available file.
        """
        if not video_files:
            return None
        # Prefer HD (height >= 720), then take whatever is available
        hd_files = [f for f in video_files if f.get("height", 0) >= 720]
        return hd_files[0] if hd_files else video_files[0]

    async def cleanup_unused_visuals(self, used_paths: List[str]):
        """
        Removes visual files that are not in the used_paths list for the current task.
        """
        print(f"🧹 Cleaning up unused visuals (keeping {len(used_paths)} files)...")
        used_set = {Path(p).resolve() for p in used_paths}
        
        count = 0
        for file in self.output_path.glob("*"):
            if file.is_file() and file.suffix in [".jpg", ".mp4"]:
                if file.resolve() not in used_set:
                    try:
                        file.unlink()
                        count += 1
                    except Exception as e:
                        print(f"  ❌ Failed to delete {file.name}: {e}")
        
        print(f"✨ Cleanup complete. Removed {count} unused files.")

visual_service = VisualService()