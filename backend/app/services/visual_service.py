import os
import httpx
from typing import List
from pathlib import Path
from app.core.config import settings

class VisualService:
    def __init__(self):
        self.api_key = settings.PEXELS_API_KEY
        self.base_url = "https://api.pexels.com/v1" # Reverted to Images API
        self.output_path = Path(settings.OUTPUT_DIR) / "visuals"
        self.output_path.mkdir(parents=True, exist_ok=True)

    async def fetch_visuals(self, keywords: List[str]) -> List[str]:
        """
        Fetches stock images from Pexels based on keywords and saves them locally.
        Returns a list of local file paths.
        """
        downloaded_paths = []
        headers = {"Authorization": self.api_key}

        async with httpx.AsyncClient(timeout=30.0) as client:
            for keyword in keywords:
                try:
                    # Search for images
                    response = await client.get(
                        f"{self.base_url}/search",
                        headers=headers,
                        params={
                            "query": keyword, 
                            "per_page": 1, 
                            "orientation": "landscape" # Best for YouTube 16:9
                        }
                    )
                    response.raise_for_status()
                    data = response.json()

                    if data.get("photos"):
                        photo = data["photos"][0]
                        # Use 'large2x' for high resolution or 'original'
                        image_url = photo["src"]["large2x"]
                        image_id = photo["id"]
                        
                        # Prepare filename
                        safe_keyword = "".join(x for x in keyword if x.isalnum() or x in " -_").strip().replace(" ", "_")
                        # Try to get extension from URL or default to .jpg
                        ext = ".jpg"
                        if ".png" in image_url.lower(): ext = ".png"
                        elif ".jpeg" in image_url.lower(): ext = ".jpeg"
                        
                        file_name = f"{safe_keyword}_{image_id}{ext}"
                        local_path = self.output_path / file_name

                        # Download image
                        print(f"Downloading image for '{keyword}'...")
                        img_response = await client.get(image_url)
                        img_response.raise_for_status()
                        
                        with open(local_path, "wb") as f:
                            f.write(img_response.content)
                        
                        downloaded_paths.append(str(local_path))
                        print(f"Successfully downloaded: {local_path}")
                    else:
                        print(f"No images found for keyword: {keyword}")

                except Exception as e:
                    print(f"Error fetching image for '{keyword}': {e}")

        return downloaded_paths

visual_service = VisualService()



