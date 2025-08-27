import os
from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from supabase import create_client
from urllib.parse import urljoin

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "hat-solutions")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


class SupabaseStorage(Storage):
    """Custom storage backend for Supabase."""

    def __init__(self):
        self.bucket = SUPABASE_BUCKET

    def _save(self, name, content):
        # Upload file to Supabase bucket
        data = content.read()
        res = supabase.storage.from_(self.bucket).upload(name, data, {"upsert": True})
        if "error" in res:
            raise Exception(f"Supabase upload error: {res['error']}")
        return name

    def _open(self, name, mode="rb"):
        # Download file from Supabase
        res = supabase.storage.from_(self.bucket).download(name)
        if isinstance(res, bytes):
            return ContentFile(res)
        raise Exception("Failed to download file from Supabase")

    def url(self, name):
        # Return public URL
        return supabase.storage.from_(self.bucket).get_public_url(name)

    def exists(self, name):
        try:
            files = supabase.storage.from_(self.bucket).list(path=name)
            return len(files) > 0
        except Exception:
            return False
