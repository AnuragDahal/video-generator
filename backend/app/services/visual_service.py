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

                    local_path = self._build_local_path(video_id, ".mp4")
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

visual_service = VisualService()