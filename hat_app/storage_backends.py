import os
from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "hat-solutions")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


class SupabaseStorage(Storage):
    """Base Supabase storage backend"""

    def __init__(self, location=""):
        self.bucket = SUPABASE_BUCKET
        self.location = location.strip("/")

    def _get_path(self, name):
        if self.location:
            return f"{self.location}/{name}"
        return name

    def _save(self, name, content):
        path = self._get_path(name)
        data = content.read()
        res = supabase.storage.from_(self.bucket).upload(path, data, {"upsert": True})
        if isinstance(res, dict) and res.get("error"):
            raise Exception(f"Supabase upload error: {res['error']}")
        return name

    def _open(self, name, mode="rb"):
        path = self._get_path(name)
        res = supabase.storage.from_(self.bucket).download(path)
        if isinstance(res, bytes):
            return ContentFile(res)
        raise Exception(f"Failed to download file: {path}")

    def url(self, name):
        path = self._get_path(name)
        return supabase.storage.from_(self.bucket).get_public_url(path)

    def exists(self, name):
        path = self._get_path(name)
        try:
            folder = os.path.dirname(path)
            files = supabase.storage.from_(self.bucket).list(folder)
            return any(f["name"] == os.path.basename(path) for f in files)
        except Exception:
            return False


class SupabaseStaticStorage(SupabaseStorage):
    def __init__(self):
        super().__init__(location="static")


class SupabaseMediaStorage(SupabaseStorage):
    def __init__(self):
        super().__init__(location="media")
