from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from supabase import create_client, Client
from django.conf import settings
import os
import logging

logger = logging.getLogger(__name__)

class SupabaseStorage(Storage):
    def __init__(self, location=None):
        self.location = location or self.location
        self.supabase = self._get_supabase_client()
        self.bucket_name = settings.SUPABASE_BUCKET

    def _get_supabase_client(self) -> Client:
        """Initialize and return Supabase client"""
        supabase_url = settings.SUPABASE_URL
        supabase_key = settings.SUPABASE_KEY
        
        if not supabase_url or not supabase_key:
            raise ValueError("Supabase URL and Key must be set in environment variables")
            
        return create_client(supabase_url, supabase_key)

    def _save(self, name, content):
        path = f"{self.location}/{name}"
        
        # Ensure we're at the beginning of the file
        if hasattr(content, 'seek') and hasattr(content, 'tell'):
            if content.tell() > 0:
                content.seek(0)
        
        data = content.read()
        
        try:
            res = self.supabase.storage.from_(self.bucket_name).upload(
                path, 
                data, 
                {"upsert": True, "content-type": self._get_content_type(name)}
            )
            
            if hasattr(res, 'error') and res.error:
                logger.error(f"Supabase upload error: {res.error}")
                raise Exception(f"Supabase upload error: {res.error}")
                
            return path
        except Exception as e:
            logger.error(f"Error uploading to Supabase: {str(e)}")
            raise

    def _get_content_type(self, filename):
        """Get content type based on file extension"""
        extension = os.path.splitext(filename)[1].lower()
        content_types = {
            '.css': 'text/css',
            '.js': 'application/javascript',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.svg': 'image/svg+xml',
            '.ico': 'image/x-icon',
        }
        return content_types.get(extension, 'application/octet-stream')

    def url(self, name):
        return f"{settings.SUPABASE_URL}/storage/v1/object/public/{self.bucket_name}/{self.location}/{name}"

    def exists(self, name):
        try:
            path = f"{self.location}/{name}"
            res = self.supabase.storage.from_(self.bucket_name).list(path)
            return len(res) > 0
        except:
            return False

    def delete(self, name):
        path = f"{self.location}/{name}"
        try:
            self.supabase.storage.from_(self.bucket_name).remove([path])
        except Exception as e:
            logger.error(f"Error deleting from Supabase: {str(e)}")
            raise

class SupabaseStaticStorage(SupabaseStorage):
    """Storage for static files (CSS, JS, Admin assets)."""
    location = "static"

class SupabaseMediaStorage(SupabaseStorage):
    """Storage for uploaded media (user files, portfolio images)."""
    location = "media"