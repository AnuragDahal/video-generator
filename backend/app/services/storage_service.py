import os
from supabase import create_client, Client
from app.core.config import settings
from pathlib import Path

class StorageService:
    def __init__(self):
        self.url = settings.SUPABASE_URL
        self.key = settings.SUPABASE_ANON_PUBLIC_KEY
        self.bucket = settings.SUPABASE_BUCKET
        self.client: Client = None
        
        if self.url and self.key:
            self.client = create_client(self.url, self.key)

    async def upload_file(self, file_path: str, content_type: str = "video/mp4") -> str:
        """
        Uploads a file to Supabase storage and returns the public URL.
        """
        if not self.client:
            print(f"Supabase storage not configured. Using local path as URL: {file_path}")
            return file_path

        p = Path(file_path)
        file_name = p.name
        
        try:
            with open(file_path, 'rb') as f:
                self.client.storage.from_(self.bucket).upload(
                    path=file_name,
                    file=f.read(),
                    file_options={"content-type": content_type, "x-upsert": "true"}
                )
            
            # Get the public URL
            response = self.client.storage.from_(self.bucket).get_public_url(file_name)
            return response
        except Exception as e:
            print(f"Error uploading to Supabase: {e}")
            return file_path

    async def upload_video(self, file_path: str) -> str:
        return await self.upload_file(file_path, "video/mp4")

    async def upload_thumbnail(self, file_path: str) -> str:
        return await self.upload_file(file_path, "image/jpeg")

storage_service = StorageService()
