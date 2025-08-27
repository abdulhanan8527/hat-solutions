from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from supabase import create_client
import os
import logging

logger = logging.getLogger(__name__)

class SupabaseStorage(Storage):
    def __init__(self, location=None):
        self.location = location or ""
        self.supabase = self._get_supabase_client()
        self.bucket_name = os.getenv("SUPABASE_BUCKET", "hat-solutions")

    def _get_supabase_client(self):
        """Initialize and return Supabase client"""
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError("Supabase URL and Key must be set in environment variables")
            
        return create_client(supabase_url, supabase_key)

    def _save(self, name, content):
        # Ensure the path is correctly formatted
        path = f"{self.location}/{name}" if self.location else name
        
        # Read content
        if hasattr(content, 'read'):
            content.seek(0)
            data = content.read()
        else:
            data = content
        
        try:
            # Upload to Supabase
            res = self.supabase.storage.from_(self.bucket_name).upload(
                path, 
                data, 
                {"upsert": True, "content-type": self._get_content_type(name)}
            )
            
            # Check for errors
            if hasattr(res, 'error') and res.error:
                logger.error(f"Supabase upload error: {res.error}")
                raise Exception(f"Supabase upload error: {res.error}")
                
            logger.info(f"Successfully uploaded {path} to Supabase")
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
            '.html': 'text/html',
            '.txt': 'text/plain',
        }
        return content_types.get(extension, 'application/octet-stream')

    def url(self, name):
        path = f"{self.location}/{name}" if self.location else name
        return f"{os.getenv('SUPABASE_URL')}/storage/v1/object/public/{self.bucket_name}/{path}"

    def exists(self, name):
        try:
            path = f"{self.location}/{name}" if self.location else name
            res = self.supabase.storage.from_(self.bucket_name).list(path)
            return len(res) > 0
        except:
            return False

    def delete(self, name):
        path = f"{self.location}/{name}" if self.location else name
        try:
            self.supabase.storage.from_(self.bucket_name).remove([path])
        except Exception as e:
            logger.error(f"Error deleting from Supabase: {str(e)}")
            raise

class SupabaseStaticStorage(SupabaseStorage):
    """Storage for static files (CSS, JS, Admin assets)."""
    def __init__(self):
        super().__init__("static")

class SupabaseMediaStorage(SupabaseStorage):
    """Storage for uploaded media (user files, portfolio images)."""
    def __init__(self):
        super().__init__("media")