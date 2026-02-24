import os
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

    async def fetch_visuals_for_scenes(self, scenes: List[Dict]) -> List[Dict]:
        """
        Downloads one best-match image per scene using keyword fallback logic.
        Keywords are ordered most-specific → least-specific by the script generator.
        Attaches local paths to each scene under 'image_paths'.
        """
        for i, scene in enumerate(scenes):
            keywords = scene.get("visual_keywords", [])
            print(f"🖼  Scene {i+1}: searching images with {len(keywords)} keyword(s)...")
            best_image = await self._fetch_best_image(keywords)
            scene["image_paths"] = [best_image] if best_image else []
            if not best_image:
                print(f"  ⚠️  Scene {i+1}: no image found for any keyword.")
        return scenes

    async def fetch_video_clips_for_scenes(self, scenes: List[Dict]) -> List[Dict]:
        """
        Downloads one best-match video clip per scene using keyword fallback logic.
        Keywords are ordered most-specific → least-specific by the script generator.
        Attaches local paths to each scene under 'video_paths'.
        """
        for i, scene in enumerate(scenes):
            keywords = scene.get("visual_keywords", [])
            print(f"🎬  Scene {i+1}: searching video clips with {len(keywords)} keyword(s)...")
            best_clip = await self._fetch_best_video(keywords)
            scene["video_paths"] = [best_clip] if best_clip else []
            if not best_clip:
                print(f"  ⚠️  Scene {i+1}: no video clip found for any keyword.")
        return scenes

    # -------------------------------------------------------------------------
    # Fallback search — tries keywords one by one, stops at first good result
    # -------------------------------------------------------------------------

    async def _fetch_best_image(self, keywords: List[str]) -> Optional[str]:
        """
        Tries each keyword in order (most specific → least specific).
        Returns the local path of the first successfully downloaded image, or None.
        """
        headers = {"Authorization": self.api_key}
        async with httpx.AsyncClient(timeout=30.0) as client:
            for keyword in keywords:
                try:
                    response = await client.get(
                        f"{self.base_url}/search",
                        headers=headers,
                        params={"query": keyword, "per_page": 3, "orientation": "landscape"}
                    )
                    response.raise_for_status()
                    photos = response.json().get("photos", [])

                    if not photos:
                        print(f"  ↳ No images for '{keyword}', trying next keyword...")
                        continue

                    # Pick the highest quality photo from results
                    photo = photos[0]
                    image_url = photo["src"]["large2x"]
                    image_id = photo["id"]

                    local_path = self._build_local_path(keyword, image_id, ".jpg")
                    if local_path.exists():
                        print(f"  ✅ Cache hit: '{keyword}'")
                        return str(local_path)

                    print(f"  ⬇️  Downloading image: '{keyword}'")
                    img_response = await client.get(image_url)
                    img_response.raise_for_status()
                    local_path.write_bytes(img_response.content)
                    return str(local_path)

                except Exception as e:
                    print(f"  ❌ Error for keyword '{keyword}': {e}")

        return None

    async def _fetch_best_video(self, keywords: List[str]) -> Optional[str]:
        """
        Tries each keyword in order (most specific → least specific).
        Returns the local path of the first successfully downloaded video clip, or None.
        Prefers HD quality (1280x720) over SD.
        """
        headers = {"Authorization": self.api_key}
        async with httpx.AsyncClient(timeout=60.0) as client:
            for keyword in keywords:
                try:
                    response = await client.get(
                        f"{self.video_base_url}/search",
                        headers=headers,
                        params={"query": keyword, "per_page": 3, "orientation": "landscape"}
                    )
                    response.raise_for_status()
                    videos = response.json().get("videos", [])

                    if not videos:
                        print(f"  ↳ No video clips for '{keyword}', trying next keyword...")
                        continue

                    # Pick the best quality video file (prefer HD)
                    video = videos[0]
                    video_id = video["id"]
                    video_file = self._pick_best_video_file(video.get("video_files", []))

                    if not video_file:
                        print(f"  ↳ No usable video file for '{keyword}', trying next keyword...")
                        continue

                    local_path = self._build_local_path(keyword, video_id, ".mp4")
                    if local_path.exists():
                        print(f"  ✅ Cache hit: '{keyword}'")
                        return str(local_path)

                    print(f"  ⬇️  Downloading video clip: '{keyword}'")
                    vid_response = await client.get(video_file["link"])
                    vid_response.raise_for_status()
                    local_path.write_bytes(vid_response.content)
                    return str(local_path)

                except Exception as e:
                    print(f"  ❌ Error for keyword '{keyword}': {e}")

        return None

    # -------------------------------------------------------------------------
    # Legacy methods (kept for backward compatibility / standalone tests)
    # -------------------------------------------------------------------------

    async def fetch_visuals(self, keywords: List[str]) -> List[str]:
        """Legacy: fetches one image per keyword (no fallback logic)."""
        paths = []
        for kw in keywords:
            result = await self._fetch_best_image([kw])
            if result:
                paths.append(result)
        return paths

    async def fetch_video_clips(self, keywords: List[str]) -> List[str]:
        """Legacy: fetches one video per keyword (no fallback logic)."""
        paths = []
        for kw in keywords:
            result = await self._fetch_best_video([kw])
            if result:
                paths.append(result)
        return paths

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    def _build_local_path(self, keyword: str, media_id: int, ext: str) -> Path:
        safe_keyword = (
            "".join(x for x in keyword if x.isalnum() or x in " -_")
            .strip()
            .replace(" ", "_")
        )[:50]  # cap length to avoid filesystem limits
        return self.output_path / f"{safe_keyword}_{media_id}{ext}"

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


visual_service = VisualService()
