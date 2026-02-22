import os
import httpx
from typing import List, Dict
from pathlib import Path
from app.core.config import settings

class VisualService:
    def __init__(self):
        self.api_key = settings.PEXELS_API_KEY
        self.base_url = "https://api.pexels.com/v1"
        self.output_path = Path(settings.OUTPUT_DIR) / "visuals"
        self.output_path.mkdir(parents=True, exist_ok=True)

    async def fetch_visuals_for_scenes(self, scenes: List[Dict]) -> List[Dict]:
        """
        Downloads images for each scene and attaches the local paths to the scene object.
        Returns the list of scenes with 'image_paths' added to each.
        """
        for i, scene in enumerate(scenes):
            keywords = scene.get("visual_keywords", [])
            if not keywords:
                scene["image_paths"] = []
                continue
            
            print(f"Processing visuals for Scene {i+1}...")
            # Fetch up to 2 images per scene to keep it dynamic
            scene_images = await self.fetch_visuals(keywords[:2])
            scene["image_paths"] = scene_images
            
        return scenes

    async def fetch_visuals(self, keywords: List[str]) -> List[str]:
        """
        Fetches stock images from Pexels based on keywords and saves them locally.
        """
        downloaded_paths = []
        headers = {"Authorization": self.api_key}

        async with httpx.AsyncClient(timeout=30.0) as client:
            for keyword in keywords:
                try:
                    response = await client.get(
                        f"{self.base_url}/search",
                        headers=headers,
                        params={"query": keyword, "per_page": 1, "orientation": "landscape"}
                    )
                    response.raise_for_status()
                    data = response.json()

                    if data.get("photos"):
                        photo = data["photos"][0]
                        image_url = photo["src"]["large2x"]
                        image_id = photo["id"]
                        
                        safe_keyword = "".join(x for x in keyword if x.isalnum() or x in " -_").strip().replace(" ", "_")
                        ext = ".jpg"
                        if ".png" in image_url.lower(): ext = ".png"
                        elif ".jpeg" in image_url.lower(): ext = ".jpeg"
                        
                        file_name = f"{safe_keyword}_{image_id}{ext}"
                        local_path = self.output_path / file_name

                        if local_path.exists():
                            downloaded_paths.append(str(local_path))
                            continue

                        print(f"Downloading image for '{keyword}'...")
                        img_response = await client.get(image_url)
                        img_response.raise_for_status()
                        
                        with open(local_path, "wb") as f:
                            f.write(img_response.content)
                        
                        downloaded_paths.append(str(local_path))
                except Exception as e:
                    print(f"Error fetching image for '{keyword}': {e}")

        return downloaded_paths

visual_service = VisualService()
