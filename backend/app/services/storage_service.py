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

    async def upload_video(self, file_path: str) -> str:
        """
        Uploads a video to Supabase storage and returns the public URL.
        """
        if not self.client:
            print("Supabase storage not configured. Using local path as URL.")
            return file_path

        p = Path(file_path)
        file_name = p.name
        
        try:
            with open(file_path, 'rb') as f:
                # Upload the file
                # Storage logic is typically sync in the current supabase-py SDK
                self.client.storage.from_(self.bucket).upload(
                    path=file_name,
                    file=f.read(),
                    file_options={"content-type": "video/mp4", "x-upsert": "true"}
                )
            
            # Get the public URL
            response = self.client.storage.from_(self.bucket).get_public_url(file_name)
            return response
        except Exception as e:
            print(f"Error uploading to Supabase: {e}")
            return file_path

storage_service = StorageService()
